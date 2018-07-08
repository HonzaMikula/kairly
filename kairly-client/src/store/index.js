import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    profile: {
      user: null,
      subscribedEditions: [], // ids
      managedEditions: [] // ids
    },
    backlog: {},
    editions: {},
    timeline: {
      issues: null, //null - not loaded, [] - loaded but empty
      cursor: null,
      loading: false,
      expandedIssues: {}
    }
  },

  mutations: {
    user(state, user) {
      state.profile.user = user
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
    subscribedEditions(state, editionIds) {
      state.profile.subscribedEditions = editionIds
    },
    managedEditions(state, editionIds) {
      state.profile.managedEditions = editionIds
    },
    appendManagedEdition(state, editionId) {
      state.profile.managedEditions.push(editionId)
    },
    removeEdition(state, editionId) {
      // remove from managed
      let idx = state.profile.managedEditions.indexOf(editionId)
      if (idx !== -1) {
        state.profile.managedEditions.splice(idx, 1)
      }
      // remove from subscribed
      idx = state.profile.subscribedEditions.indexOf(editionId)
      if (idx !== -1) {
        state.profile.subscribedEditions.splice(idx, 1)
      }
      Vue.delete(state.editions, editionId)
    },
    edition(state, edition) {
      state.editions = {...state.editions, [edition.fullName]: edition}
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
    user: state => state.profile.user,
    loadingUser: state => state.profile.user === null, // Unauthorized -> user === false
    subscribedEditions: state => state.profile.subscribedEditions.map(id => state.editions[id]),
    managedEditions: state => state.profile.managedEditions.map(id => state.editions[id]),
    backlog: state => state.backlog,
    edition: state => id => state.editions[id]
  },

  actions,
  strict: process.env.NODE_ENV !== 'production'
})
