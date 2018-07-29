import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    profile: {
      user: null,
      managedEditions: [] // ids
    },
    subscriptions: {
      authors: {},
      editions: {}
    },
    backlog: {},
    editions: {},
    timeline: {
      issues: null, //null - not loaded, [] - loaded but empty
      cursor: null,
      loading: false,
      expandedIssues: {}
    },
    error: null,
    show404: false
  },

  mutations: {
    user(state, user) {
      state.profile.user = user
    },
    backlog(state, backlog) {
      state.backlog = backlog
    },
    backlogAdd(state, { postId, editionId }) {
      const currEditions = state.backlog[postId] || {}
      state.backlog = {
        ...state.backlog,
        [postId]: {...currEditions, [editionId]: 'C'}
      }
    },
    backlogSetPostState(state, { postId, editionId, val }) {
      const currEditions = state.backlog[postId] || {}
      state.backlog = {
        ...state.backlog,
        [postId]: {...currEditions, [editionId]: val}
      }
    },
    backlogRemove(state, { postId, editionId }) {
      // TODO this would be nice move to utils function
      // we need shallow copy with updated nested object
      let currEditions = {...state.backlog[postId]}
      delete currEditions[editionId]

      const backlog = {...state.backlog}
      if (Object.keys(currEditions).length) {
        backlog[postId] = currEditions
      } else {
        delete backlog[postId]
      }
      state.backlog = backlog
    },
    subscriptions(state, subscriptions) {
      state.subscriptions = subscriptions
    },
    addEditionSubscription(state, fullName) {
      Vue.set(state.subscriptions.editions, fullName, true)
    },
    removeEditionSubscription(state, fullName) {
      Vue.delete(state.subscriptions.editions, fullName)
    },
    addAuthorSubscription(state, { authorId, periodicity }) {
      Vue.set(state.subscriptions.authors, authorId, periodicity)
    },
    removeAuthorSubscription(state, { authorId }) {
      Vue.delete(state.subscriptions.authors, authorId)
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
      if (state.subscriptions.editions[editionId]) {
        Vue.delete(state.subscriptions.editions, editionId)
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
    expandIssue(state, issueId) {
      state.timeline.expandedIssues = {
        ...state.timeline.expandedIssues,
        [issueId]: true
      }
    },
    showError(state, msg) {
      state.error = msg
    },
    show404(state, value=true) {
      state.show404 = value
    }
  },

  getters: {
    user: state => state.profile.user,
    loadingUser: state => state.profile.user === null, // Unauthorized -> user === false
    //subscribedEditions: state => state.profile.subscribedEditions.map(id => state.editions[id]),
    managedEditions: state => state.profile.managedEditions.map(id => state.editions[id]),
    backlog: state => state.backlog,
    edition: state => id => state.editions[id]
  },

  actions,
  strict: process.env.NODE_ENV !== 'production'
})
