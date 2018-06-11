import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    managedAuthors: [],
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
    managedAuthors(state, authors) {
      state.managedAuthors = authors
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
    edition: state => id => state.editions[id],
    isManagedAuthor: state => slug => state.managedAuthors.indexOf(slug) !== -1
  },

  actions,
  strict: process.env.NODE_ENV !== 'production'
})
