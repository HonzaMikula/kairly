import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    backlog: {},
    managedEditions: [],
    editions: {},
    allEditionsLoaded: false,
    timeline: {
      issues: null, //null - not loaded, [] - loaded but empty
      cursor: null,
      loading: false,
      expandedIssues: {}
    }
  },

  mutations: {
    user(state, user) {
      state.user = user
    },
    backlog(state, backlog) {
      state.backlog = backlog
    },
    backlogAdd(state, { postId, editionId }) {
      const currEditions = state.backlog[postId] || []
      state.backlog = {...state.backlog, [postId]: [...currEditions, editionId]}
    },
    backlogRemove(state, { postId, editionId }) {
      // TODO this would be nice move to utils function
      // we need shallow copy with updated nested object
      let currEditions = [...state.backlog[postId]] || []
      const idx = currEditions.findIndex(i => i == editionId)
      if (idx !== -1) {
        currEditions.splice(idx, 1)
      }
      const backlog = {...state.backlog}
      if (currEditions.length) {
        backlog[postId] = currEditions
      } else {
        delete backlog[postId]
      }
      state.backlog = backlog
    },
    managedEditions(state, editions) {
      state.managedEditions = editions
    },
    appendManagedEdition(state, edition) {
      state.managedEditions.push(edition)
    },
    removeManagedEdition(state, edition) {
      const idx = state.managedEditions.findIndex(e => e.id === edition.id)
      if (idx !== -1) {
        state.managedEditions.splice(idx, 1)
      }
    },
    allEditions(state, editions) {
      editions.forEach(edition => {
        state.editions[edition.id] = edition
      })
      state.allEditionsLoaded = true
    },
    edition(state, edition) {
      state.editions = {...state.editions, [edition.id]: edition}
    },
    timelineRequested(state) {
      state.timeline.loading = true
    },
    timelineReceived(state, { issues, cursor }) {
      if (state.timeline.issues === null) {
        state.timeline.issues = []
      }
      issues.forEach(issue => state.timeline.issues.push(issue))
      state.timeline.cursor = cursor
      state.timeline.loading = false
    },
    invalidateTimeline(state) {
      state.timeline.issues = null
      state.timeline.cursor = null
      state.timeline.loading = false
      state.timeline.expandedIssues = {}
    },
    expandIssue (state, issueId) {
      state.timeline.expandedIssues = {
        ...state.timeline.expandedIssues,
        [issueId]: true
      }
    }
  },

  getters: {
    loadingUser: state => state.user === null, // Unauthorized -> user === false
    allEditions: state => state.allEditionsLoaded ? Object.values(state.editions) : null,
    edition: state => id => state.editions[id]
  },

  actions,
  strict: process.env.NODE_ENV !== 'production'
})
