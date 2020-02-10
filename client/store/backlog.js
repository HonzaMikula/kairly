import Vue from 'vue'

let reorderPostScheduled = false

export const state = () => ({
  userBacklog: null,
  newspaperBacklog: {},
})

async function _postBackLog(state, fullName) {
  const backlog = state.newspaperBacklog[fullName]
  await this.$axios.$post(`/newspapers/${fullName}/backlog`, {
    upcoming: backlog.upcoming.map(log => log.post.id),
    next: backlog.next.map(log => log.post.id),
    considered: backlog.considered.map(log => log.post.id)
  })
}

export const actions = {
  async loadUserBacklog({ commit, state }) {
    if (state.userBacklog) {
      return state.userBacklog
    }
    const { backlog } = await this.$axios.$get('/backlog')
    Object.entries(backlog).forEach(([postId, newspapers]) => {
      Object.entries(newspapers).forEach(([newspaperId, value]) => {
        if (value === 1) {
          backlog[postId][newspaperId] = 'next'
        } else if (value === 2) {
          backlog[postId][newspaperId] = 'upcoming'
        } else {
          backlog[postId][newspaperId] = 'considered'
        }
      })
    })

    commit('userBacklog', backlog)
    return backlog
  },

  async loadNewspaperBacklog({ commit }, fullName) {
    const { backlogs, currentMonth } = await this.$axios.$get(`/newspapers/${fullName}/backlog`)

    Object.values(backlogs).forEach(bl => {
      // TODO save layout to store
      commit('newspaperBacklog', { fullName, section: bl.name, backlog: bl})
    })
    commit('newspaperBacklogStats', { fullName, currentMonthStats: currentMonth })

  },

  async moveUp({ commit, state }, { newspaper, source, target, postId }) {
    const { fullName } = newspaper
    commit('moveUp', { fullName, source, target, postId})
    _postBackLog.call(this, state, fullName)
  },

  async moveDown({ commit, state }, { newspaper, source, target, postId }) {
    const { fullName } = newspaper
    commit('moveDown', { fullName, source, target, postId})
    _postBackLog.call(this, state, fullName)
  },

  async reorder({ commit, state }, { newspaper, source, posts }) {
    const { fullName } = newspaper
    commit('reorder', { fullName, source, posts})
    if (!reorderPostScheduled) {
      reorderPostScheduled = true
      Vue.nextTick(() => {
        reorderPostScheduled = false
        _postBackLog.call(this, state, fullName)
      })
    }
  },

  async add({ commit }, { newspaper, post, source }) {
    // TODO to have better user experience, post can be added immediately
    // and reverted when api call fails
    await this.$axios.put(`/newspapers/${newspaper.fullName}/backlog`, {post: post.id})
    commit('prepend', {
      fullName: newspaper.fullName,
      post,
      source
    })

    this.$ga.event({
      eventCategory: 'Consider for newspaper',
      eventAction: newspaper.fullName
    })
  },

  async remove({ commit }, { newspaper, source, postId }) {
    // TODO to have better user experience, post can be removed immediately
    // and reverted when api call fails
    const { fullName } = newspaper
    await this.$axios.delete(`/newspapers/${fullName}/backlog`, { data: { post: postId } })

    commit('remove', {
      fullName: fullName,
      source,
      postId,
    })

    this.$ga.event({
      eventCategory: 'Stop considering for newspaper',
      eventAction: fullName
    })
  },

  async addLink({ commit, state }, { newspaper, url }) {
    const { fullName } = newspaper
    const resp = await this.$axios.$post(`/newspapers/${newspaper.fullName}/backlog/links`, {url})
    if (resp.post) {
      commit('append', {
        fullName,
        source: 'considered',
        post: resp.post
      })

      this.$ga.event({
        eventCategory: 'Consider for newspaper',
        eventAction: fullName
      })
    }
  },

  async saveEditorial({ commit}, { newspaperId, source, postId, editorial: payload}) {
    const editorial = await this.$axios.$post(`/newspapers/${newspaperId}/editorials/${postId}`, payload)
    commit('updateEditorial', { fullName: newspaperId, source, postId, editorial })
    return editorial
  },

  async saveEditorialPosition({ commit }, { newspaperId, source, postId, position }) {
    const editorial = await this.$axios.$patch(`/newspapers/${newspaperId}/editorials/${postId}`, {position})
    commit('updateEditorial', { fullName: newspaperId, source, postId, editorial })
    return editorial
  },

  async removeEditorial({ commit }, { newspaperId, source, postId}) {
    await this.$axios.$delete(`/newspapers/${newspaperId}/editorials/${postId}`)
    commit('updateEditorial', { fullName: newspaperId, source, postId, editorial: null })
  },
}

export const mutations = {
  resetState(state) {
    state.userBacklog = null
    state.newspaperBacklog = null
  },

  userBacklog(state, backlog) {
    state.userBacklog = backlog
  },

  newspaperBacklog( state, { fullName, section, backlog }) {
    if (state.newspaperBacklog[fullName]) {
      Vue.set(state.newspaperBacklog[fullName], section, backlog)
    } else {
      Vue.set(state.newspaperBacklog, fullName, { [section]: backlog })
    }
  },
  newspaperBacklogStats( state, { fullName, currentMonthStats}) {
    // TODO use different key then newspaperBacklog
    if (state.newspaperBacklog[fullName]) {
      Vue.set(state.newspaperBacklog[fullName], 'currentMonthStats', currentMonthStats)
    } else {
      Vue.set(state.newspaperBacklog, fullName, { currentMonthStats })
    }
  },
  updateEditorial(state, { fullName, source, postId, editorial }) {
    const backlog = state.newspaperBacklog[fullName]
    let posts = backlog[source]
    const idx = posts.findIndex(log => log.post.id === postId)
    posts[idx].editorial = editorial
  },

  remove(state, { fullName, source, postId }) {
    const postBacklog = state.userBacklog[postId] || {}
    delete postBacklog[fullName]
    Vue.set(state.userBacklog, postId, {...postBacklog})

    const newspaperBacklog = state.newspaperBacklog[fullName]
    if (newspaperBacklog) {
      let posts = newspaperBacklog[source]
      const idx = posts.findIndex(log => log.post.id === postId)
      posts.splice(idx, 1)
    }
  },
  append(state, { fullName, source, post }) {
    const postBacklog = state.userBacklog[post.id] || {}
    Vue.set(state.userBacklog, post.id, { ...postBacklog, [fullName]: source })

    const newspaperBacklog = state.newspaperBacklog[fullName]
    if (newspaperBacklog) {
      newspaperBacklog[source].push({ post: post, editorial: null })
    }
  },
  prepend(state, { fullName, source, post }) {
    const postBacklog = state.userBacklog[post.id] || {}
    Vue.set(state.userBacklog, post.id, { ...postBacklog, [fullName]: source })

    const newspaperBacklog = state.newspaperBacklog[fullName]
    if (newspaperBacklog) {
      newspaperBacklog[source].unshift({ post: post, editorial: null })
    }
  },
  moveUp(state, { fullName, source, target, postId }) {
    const backlog = state.newspaperBacklog[fullName]
    let posts = backlog[source]
    const idx = posts.findIndex(log => log.post.id === postId)
    const post = posts[idx]
    if (idx === 0 || target !== null) {
      if (target === null) {
        target = (source === 'considered' ? 'next' : 'upcoming')
      }
      const targetPosts = backlog[target]
      posts.splice(idx, 1)
      targetPosts.push(post)
    } else {
      Vue.set(posts, idx, posts[idx - 1])
      Vue.set(posts, idx - 1, post)
    }
  },
  moveDown(state, { fullName, source, target, postId }) {
    const backlog = state.newspaperBacklog[fullName]
    let posts = backlog[source]
    const idx = posts.findIndex(log => log.post.id === postId)
    const post = posts[idx]
    if (idx === posts.length - 1 || target !== null) {
      if (target === null) {
        target =  source == 'upcoming' ? 'next' : 'considered'
      }
      const targetPosts = backlog[target]
      posts.splice(idx, 1)
      targetPosts.unshift(post)
    } else {
      Vue.set(posts, idx, posts[idx + 1])
      Vue.set(posts, idx + 1, post)
    }
  },
  reorder(state, { fullName, source, posts }) {
    const backlog = state.newspaperBacklog[fullName]
    backlog[source] = posts
  },
}
