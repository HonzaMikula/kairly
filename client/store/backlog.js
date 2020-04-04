import Vue from 'vue'
import isString from 'lodash/isString'
import keyBy from 'lodash/keyBy'
import debounce from 'lodash/debounce'

let reorderPostScheduled = false
const UPPERMOST_BACKLOG = 'upcoming'
const BOTTOMMOST_BACKLOG = 'considered'

export const state = () => ({
  userBacklog: null,
  newspaperBacklog: {},
  selection: {} // newspaper editor selection
})

const getItemPostIds = (item) => {
  const postIds = []
  if (item.type === 'box') {
    item.columns.forEach(col => col.posts.forEach(p => postIds.push(p.id)))
  }
  if (item.type === 'post') {
    postIds.push(item.id)
  }
  return postIds
}

// TODO flush on page change
const deboundedSave = debounce(($axios, fullName, data) => {
  $axios.$post(`/newspapers/${fullName}/backlog`, data, { progress: false })
}, 500)

export const actions = {
  async loadUserBacklog ({ commit, state }) {
    if (state.userBacklog) {
      return state.userBacklog
    }
    const { backlog } = await this.$axios.$get('/backlog')
    commit('userBacklog', backlog)
    return backlog
  },

  async loadNewspaperBacklog ({ commit }, fullName) {
    const { backlogs, posts, currentMonth } = await this.$axios.$get(`/newspapers/${fullName}/backlog`)

    commit('newspaperBacklogPosts', { fullName, posts })
    commit('newspaperBacklogStats', { fullName, currentMonthStats: currentMonth })

    Object.values(backlogs).forEach(bl => {
      bl.layout = bl.layout.map(item => {
        if (Array.isArray(item)) {
          const css = isString(item[0]) ? item[0] : null
          const columns = css === null ? item : item.slice(1)
          return {
            id: Math.random().toString(36).substring(2),
            type: 'box',
            css,
            columns: columns.map(c => {
              return {
                css: isString(c[0]) ? c[0] : '',
                posts: (isString(c[0]) ? c.slice(1) : c).map(item => ({ type: 'post', id: item.post }))
              }
            })
          }
        }
        if (item.post) {
          return { type: 'post', id: item.post }
        }
        if (item.header !== undefined) { // header can be null
          return { type: 'header', id: Math.random().toString(36).substring(2), title: item.header }
        }
        throw new Error('Unknown type')
      })
      commit('newspaperBacklog', { fullName, section: bl.name, backlog: bl })
    })
  },

  save ({ state }, { newspaper }) {
    const { fullName } = newspaper

    function serialize (layout) {
      return layout.map(item => {
        if (item.type === 'post') { return { post: item.id } }
        if (item.type === 'header') { return { header: item.title } }
        if (item.type === 'box') {
          const box = [item.css]
          item.columns.forEach(col => {
            const data = []
            if (col.css && col.css !== '') {
              data.push(col.css)
            }
            col.posts.forEach(p => data.push({ post: p.id }))
            box.push(data)
          })
          return box
        }
        throw new Error('Unknown type')
      })
    }

    const backlog = state.newspaperBacklog[fullName]
    const data = {
      upcoming: serialize(backlog.upcoming.layout),
      next: serialize(backlog.next.layout),
      considered: serialize(backlog.considered.layout)
    }

    deboundedSave(this.$axios, fullName, data)
  },

  reorder ({ commit, dispatch }, { newspaper, target, ordering }) {
    commit('reorder', { newspaper, target, ordering })
    if (!reorderPostScheduled) {
      reorderPostScheduled = true
      Vue.nextTick(() => {
        reorderPostScheduled = false
        dispatch('save', { newspaper })
      })
    }
  },

  async add ({ state, commit, dispatch }, { newspaper, post, target }) {
    if (!state.newspaperBacklog[newspaper.fullName]) {
      await dispatch('loadNewspaperBacklog', newspaper.fullName)
    }
    commit('splice', {
      newspaper,
      target,
      items: [{ id: post.id, type: 'post' }],
      index: 0,
      deleteCount: 0
    })
    dispatch('save', { newspaper })

    this.$ga.event({
      eventCategory: 'Consider for newspaper',
      eventAction: newspaper.fullName
    })
  },

  async remove ({ state, commit, dispatch }, { newspaper, source, post }) {
    if (!state.newspaperBacklog[newspaper.fullName]) {
      await dispatch('loadNewspaperBacklog', newspaper.fullName)
    }
    commit('remove', {
      newspaper,
      source,
      postId: post.id,
    })
    dispatch('save', { newspaper })

    this.$ga.event({
      eventCategory: 'Stop considering for newspaper',
      eventAction: newspaper.fullName
    })
  },

  removeSelectedBox ({ commit, dispatch, getters }, { newspaper }) {
    const sources = getters.getSelectedBoxes(newspaper).slice()
    sources.reverse()
    sources.forEach(item => {
      commit('remove', {
        newspaper,
        source: item.source,
        index: item.index
      })
    })

    dispatch('save', { newspaper })
  },

  async addLink ({ state, commit, dispatch }, { newspaper, target, index, columnIndex, url }) {
    const { post } = await this.$axios.$post('/external-links', { url })
    if (post) {
      commit('registerPost', { newspaper, post })
      const item = { id: post.id, type: 'post' }
      if (columnIndex === undefined) {
        commit('splice', {
          newspaper,
          target,
          items: [item],
          index,
          deleteCount: 0
        })
      } else {
        const box = state.newspaperBacklog[newspaper.fullName][target].layout[index]
        commit('setBacklogItem', {
          newspaper,
          target,
          index,
          item: {
            ...box,
            columns: box.columns.map((col, idx) => {
              return {
                ...col,
                posts: columnIndex === idx ? [...col.posts, item] : col.posts
              }
            })
          }
        })
      }
      dispatch('save', { newspaper })

      this.$ga.event({
        eventCategory: 'Add external article',
        eventAction: url,
        eventLabel: newspaper.fullName
      })
    }
  },

  moveSelectionUp ({ commit, dispatch, getters }, { newspaper }) {
    const sources = getters.getSelectedBoxes(newspaper)
    let prevSource = null
    let selectedBefore = 0
    sources.forEach(item => {
      if (prevSource !== item.source) {
        prevSource = item.source
        selectedBefore = 0
      }
      const index = item.index - selectedBefore
      if (item.source === UPPERMOST_BACKLOG && index === 0) {
        return
      }

      commit('moveUp', {
        newspaper,
        source: item.source,
        index,
        target: null
      })
      if (index === 0) {
        selectedBefore++
      }
    })
    dispatch('save', { newspaper })
  },

  moveSelectionDown ({ state, commit, dispatch, getters }, { newspaper, target }) {
    const { fullName } = newspaper
    let sources = getters.getSelectedBoxes(newspaper).slice()
    sources.reverse()
    if (target) {
      sources = sources.filter(({ source }) => source !== target)
    }

    let consideredSkipIndex = state.newspaperBacklog[fullName][BOTTOMMOST_BACKLOG].layout.length - 1
    sources.forEach(item => {
      if (item.source === BOTTOMMOST_BACKLOG && item.index === consideredSkipIndex) {
        consideredSkipIndex--
        return
      }

      commit('moveDown', {
        newspaper,
        target,
        source: item.source,
        index: item.index
      })
    })

    if (target) {
      commit('cleanSelection')
    }

    dispatch('save', { newspaper })
  },

  moveSelectionToUpcomingTop ({ commit, dispatch, getters }, { newspaper }) {
    const sources = getters.getSelectedBoxes(newspaper).slice()
    sources.reverse()
    let selectedBefore = 0
    sources.forEach(item => {
      let index = item.index
      if (item.source === UPPERMOST_BACKLOG) {
        index += selectedBefore
      }
      commit('moveUp', {
        newspaper,
        source: item.source,
        index,
        target: UPPERMOST_BACKLOG,
        top: true
      })

      selectedBefore++
    })
    commit('cleanSelection')
    dispatch('save', { newspaper })
  },

  moveSelectionToUpcomingBottom ({ commit, dispatch, getters }, { newspaper }) {
    const sources = getters.getSelectedBoxes(newspaper)
    let prevSource = null
    let selectedBefore = 0
    sources.forEach(item => {
      if (prevSource !== item.source) {
        selectedBefore = 0
        prevSource = item.source
      }

      const index = item.index - selectedBefore
      commit('moveUp', {
        newspaper,
        source: item.source,
        index,
        target: UPPERMOST_BACKLOG,
      })

      selectedBefore++
    })

    commit('cleanSelection')
    dispatch('save', { newspaper })
  },

  makeBoxFromSelection ({ commit, dispatch, getters }, { newspaper, layout, columnsStyle }) {
    if (columnsStyle.length !== getters.getSelection.length) {
      return
    }

    const sources = getters.getSelectedBoxes(newspaper).slice()
    const columns = []
    for (let i = 0; i < sources.length; i++) {
      const { box } = sources[i]
      if (box.type !== 'post') {
        // only posts can be added to box
        return
      }
      columns.push({
        css: columnsStyle[i],
        posts: [box]
      })
    }

    const boxItem = {
      id: Math.random().toString(36).substring(2),
      type: 'box',
      css: layout,
      columns
    }

    sources.reverse()
    for (let i = 0; i < sources.length; i++) {
      const item = sources[i]
      if (i === sources.length - 1) {
        // newspaper, target, index, items, deleteCount
        commit('splice', {
          newspaper,
          target: item.source,
          index: item.index,
          items: [boxItem],
          deleteCount: 1
        })
      } else {
        commit('remove', {
          newspaper,
          source: item.source,
          index: item.index
        })
      }
    }

    commit('cleanSelection')
    dispatch('save', { newspaper })
  }
}

export const mutations = {
  resetState (state) {
    state.userBacklog = null
    state.newspaperBacklog = null
  },

  userBacklog (state, backlog) {
    state.userBacklog = backlog
  },

  newspaperBacklog (state, { fullName, section, backlog }) {
    if (state.newspaperBacklog[fullName]) {
      Vue.set(state.newspaperBacklog[fullName], section, backlog)
    } else {
      Vue.set(state.newspaperBacklog, fullName, { [section]: backlog })
    }
  },

  newspaperBacklogPosts (state, { fullName, posts }) {
    if (state.newspaperBacklog[fullName]) {
      Vue.set(state.newspaperBacklog[fullName], '$posts', posts)
    } else {
      Vue.set(state.newspaperBacklog, fullName, { $posts: posts })
    }
  },

  newspaperBacklogStats (state, { fullName, currentMonthStats }) {
    // TODO use different key then newspaperBacklog
    if (state.newspaperBacklog[fullName]) {
      Vue.set(state.newspaperBacklog[fullName], 'currentMonthStats', currentMonthStats)
    } else {
      Vue.set(state.newspaperBacklog, fullName, { currentMonthStats })
    }
  },

  registerPost (state, { newspaper, post }) {
    const { fullName } = newspaper
    const { $posts } = state.newspaperBacklog[fullName]
    Vue.set($posts, post.id, post)
  },

  updatePost (state, { post }) {
    Object.values(state.newspaperBacklog).forEach(({ $posts }) => {
      if ($posts[post.id]) {
        $posts[post.id] = { ...$posts[post.id], ...post }
      }
    })
  },

  // THIS will be not working from timeline
  remove (state, { newspaper, source, index = null, postId = null }) {
    if (index === null && postId === null) {
      throw new Error('Index or post id must specified')
    }
    const { fullName } = newspaper
    const newspaperBacklog = state.newspaperBacklog[fullName]
    const { layout } = newspaperBacklog[source]

    if (index === null) {
      index = layout.findIndex(p => p.id === postId)
      if (index === -1) {
        return
      }
    }

    const item = layout[index]
    layout.splice(index, 1)

    getItemPostIds(item).forEach(id => {
      const postBacklog = state.userBacklog[id] || {}
      Vue.delete(postBacklog, fullName)
    })

    return item
  },

  setBacklogItem (state, { newspaper, target, index, item }) {
    const { fullName } = newspaper
    const newspaperBacklog = state.newspaperBacklog[fullName]
    const { layout } = newspaperBacklog[target]
    Vue.set(layout, index, item)

    getItemPostIds(item).forEach(id => {
      const postBacklog = state.userBacklog[id] || {}
      Vue.set(state.userBacklog, id, { ...postBacklog, [fullName]: target })
    })
  },

  append (state, { newspaper, target, item }) {
    const { fullName } = newspaper
    const newspaperBacklog = state.newspaperBacklog[fullName]
    const { layout } = newspaperBacklog[target]
    layout.push(item)

    getItemPostIds(item).forEach(id => {
      const postBacklog = state.userBacklog[id] || {}
      Vue.set(state.userBacklog, id, { ...postBacklog, [fullName]: target })
    })
  },

  splice (state, { newspaper, target, index, items, deleteCount }) {
    const { fullName } = newspaper
    const newspaperBacklog = state.newspaperBacklog[fullName]
    const { layout } = newspaperBacklog[target]

    const removedItems = layout.splice(index, deleteCount, ...items)
    removedItems.forEach(item => {
      getItemPostIds(item).forEach(id => {
        const postBacklog = state.userBacklog[id] || {}
        Vue.delete(postBacklog, fullName)
      })
    })

    items.forEach(item => {
      getItemPostIds(item).forEach(id => {
        const postBacklog = state.userBacklog[id] || {}
        Vue.set(state.userBacklog, id, { ...postBacklog, [fullName]: target })
      })
    })

    return removedItems
  },

  moveUp (state, { newspaper, source, target, top = false, index }) {
    const { fullName } = newspaper
    const backlog = state.newspaperBacklog[fullName]
    const sourceLayout = backlog[source].layout
    const box = sourceLayout[index]
    if (index === 0 || target !== null) {
      if (target === null) {
        target = (source === BOTTOMMOST_BACKLOG ? 'next' : UPPERMOST_BACKLOG)
      }
      const targetLayout = backlog[target].layout
      sourceLayout.splice(index, 1)
      if (top) {
        targetLayout.unshift(box)
      } else {
        targetLayout.push(box)
      }
    } else {
      Vue.set(sourceLayout, index, sourceLayout[index - 1])
      Vue.set(sourceLayout, index - 1, box)
    }
  },

  moveDown (state, { newspaper, source, target, index }) {
    const { fullName } = newspaper
    const backlog = state.newspaperBacklog[fullName]
    const sourceLayout = backlog[source].layout
    const box = sourceLayout[index]
    if (index === sourceLayout.length - 1 || target !== null) {
      if (target === null) {
        target = source === UPPERMOST_BACKLOG ? 'next' : BOTTOMMOST_BACKLOG
      }
      const targetLayout = backlog[target].layout
      sourceLayout.splice(index, 1)
      targetLayout.unshift(box)
    } else {
      Vue.set(sourceLayout, index, sourceLayout[index + 1])
      Vue.set(sourceLayout, index + 1, box)
    }
  },

  reorder (state, { newspaper, target, ordering }) {
    const backlog = state.newspaperBacklog[newspaper.fullName]
    // need to search bettween all backlogs because post can be dragged between them
    const posts = {
      ...keyBy(backlog[BOTTOMMOST_BACKLOG].layout, 'id'),
      ...keyBy(backlog[UPPERMOST_BACKLOG].layout, 'id'),
      ...keyBy(backlog.next.layout, 'id')
    }
    backlog[target].layout = ordering.map(id => posts[id])
  },

  select (state, id) {
    Vue.set(state.selection, id, true)
  },

  unselect (state, id) {
    Vue.delete(state.selection, id)
  },

  cleanSelection (state) {
    state.selection = {}
  },
}

export const getters = {
  getSelectedBoxes: (state, getters) => newspaper => {
    const { fullName } = newspaper
    const backlogNames = [UPPERMOST_BACKLOG, 'next', BOTTOMMOST_BACKLOG]
    const sources = []
    backlogNames.forEach(name => {
      const { layout } = state.newspaperBacklog[fullName][name]
      layout.forEach((box, index) => {
        if (getters.getSelection.includes('' + box.id)) {
          sources.push({
            source: name,
            index,
            box,
          })
        }
      })
    })
    return sources
  },

  getSelection: state => {
    return Object.keys(state.selection)
  },
}
