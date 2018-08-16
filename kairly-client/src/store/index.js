import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import { analyticsMiddleware } from 'vue-analytics'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    profile: {
      user: null,
      managedNewspapers: [] // ids
    },
    subscriptions: {
      authors: {},
      newspapers: {}
    },
    backlog: {},
    newspapers: {},
    timeline: {
      issues: null, //null - not loaded, [] - loaded but empty
      cursor: null,
      loading: false,
      expandedIssues: {}
    },
    messages: {
      error: null,
      success: null,
    },
    show404: false
  },

  mutations: {
    user(state, user) {
      state.profile.user = user
    },
    backlog(state, backlog) {
      state.backlog = backlog
    },
    backlogAdd(state, { postId, newspaperId }) {
      const currNewspapers = state.backlog[postId] || {}
      state.backlog = {
        ...state.backlog,
        [postId]: {...currNewspapers, [newspaperId]: 'C'}
      }
    },
    backlogSetPostState(state, { postId, newspaperId, val }) {
      const currNewspapers = state.backlog[postId] || {}
      state.backlog = {
        ...state.backlog,
        [postId]: {...currNewspapers, [newspaperId]: val}
      }
    },
    backlogRemove(state, { postId, newspaperId }) {
      // TODO this would be nice move to utils function
      // we need shallow copy with updated nested object
      let currNewspapers = {...state.backlog[postId]}
      delete currNewspapers[newspaperId]

      const backlog = {...state.backlog}
      if (Object.keys(currNewspapers).length) {
        backlog[postId] = currNewspapers
      } else {
        delete backlog[postId]
      }
      state.backlog = backlog
    },
    subscriptions(state, subscriptions) {
      state.subscriptions = subscriptions
    },
    addNewspaperSubscription(state, {fullName}) {
      Vue.set(state.subscriptions.newspapers, fullName, true)
    },
    removeNewspaperSubscription(state, {fullName}) {
      Vue.delete(state.subscriptions.newspapers, fullName)
    },
    addAuthorSubscription(state, { authorId, periodicity }) {
      Vue.set(state.subscriptions.authors, authorId, periodicity)
    },
    removeAuthorSubscription(state, { authorId }) {
      Vue.delete(state.subscriptions.authors, authorId)
    },
    managedNewspapers(state, newspaperIds) {
      state.profile.managedNewspapers = newspaperIds
    },
    appendManagedNewspaper(state, {newspaper}) {
      state.profile.managedNewspapers.push(newspaper.fullName)
    },
    removeNewspaper(state, {newspaper}) {
      // remove from managed
      let idx = state.profile.managedNewspapers.indexOf(newspaper.fullName)
      if (idx !== -1) {
        state.profile.managedNewspapers.splice(idx, 1)
      }
      // remove from subscribed
      if (state.subscriptions.newspapers[newspaper.fullName]) {
        Vue.delete(state.subscriptions.newspapers, newspaper.fullName)
      }

      Vue.delete(state.newspapers, newspaper.fullName)
    },
    newspaper(state, newspaper) {
      state.newspapers = {...state.newspapers, [newspaper.fullName]: newspaper}
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
    expandIssue(state, { issueId }) {
      state.timeline.expandedIssues = {
        ...state.timeline.expandedIssues,
        [issueId]: true
      }
    },
    showError(state, msg) {
      state.messages = {...state.messages, error: msg }
    },
    showSuccess(state, msg) {
      state.messages = {...state.messages, success: msg }
    },
    show404(state, value=true) {
      state.show404 = value
    }
  },

  getters: {
    user: state => state.profile.user,
    loadingUser: state => state.profile.user === null, // Unauthorized -> user === false
    //subscribedNewspapers: state => state.profile.subscribedNewspapers.map(id => state.newspapers[id]),
    managedNewspapers: state => state.profile.managedNewspapers.map(id => state.newspapers[id]),
    backlog: state => state.backlog,
    newspaper: state => id => state.newspapers[id]
  },

  actions,
  strict: process.env.NODE_ENV !== 'production',
  plugins: [
    analyticsMiddleware
  ]
})
