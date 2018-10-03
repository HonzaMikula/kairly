import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions'
import { analyticsMiddleware } from 'vue-analytics'

// TODO use Immer for state manipulation. Or better, modular state from Nuxt

const createStore = () => {
  return new Vuex.Store({
    state: {
      subscriptions: null,
      backlog: null,
      newspapers: {},
      authors: {},
      timelineExpandedIssues: {},
      timeline: {
        // issues: null, //null - not loaded, [] - loaded but empty
        // cursor: null,
        // loading: false,
      },
      messages: {
        error: null,
        success: null,
      }
    },

    mutations: {
      user(state, { user }) {
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
      newspaperSubscription(state, {subscription}) {
        if (state.subscriptions) {
          state.subscriptions = {
            ...state.subscriptions,
            newspapers: {...state.subscriptions.newspapers, ...subscription}
          }
        }
      },
      authorSubscription(state, { subscription }) {
        if (state.subscriptions) {
          state.subscriptions = {
            ...state.subscriptions,
            authors: {...state.subscriptions.authors, ...subscription}
          }
        }
      },
      appendOwnedNewspaper(state, { newspaper }) {
        state.auth.user.newspapers.push(newspaper)
      },
      removeNewspaper(state, { newspaper }) {
        // remove from owned
        let idx = state.auth.user.newspapers.findIndex(n => n.fullName === newspaper.fullName)
        if (idx !== -1) {
          state.auth.user.newspapers.splice(idx, 1)
        }
        // remove from subscribed if loaded
        if (state.subscriptions && state.subscriptions.newspapers[newspaper.fullName]) {
          Vue.delete(state.subscriptions.newspapers, newspaper.fullName)
        }

        Vue.delete(state.newspapers, newspaper.fullName)
      },
      newspaper(state, { newspaper }) {
        state.newspapers = {...state.newspapers, [newspaper.fullName]: newspaper}
      },
      // timelineRequested(state) {
      //   state.timeline.loading = true
      // },
      // timelineReceived(state, { issues, cursor }) {
      //   if (state.timeline.issues === null) {
      //     state.timeline.issues = []
      //   }
      //   issues.forEach(issue => state.timeline.issues.push(issue))
      //   state.timeline.cursor = cursor
      //   state.timeline.loading = false
      // },
      invalidateTimeline(state) {
        // state.timeline.issues = null
        // state.timeline.cursor = null
        // state.timeline.loading = false
        // state.timeline.expandedIssues = {}
      },
      expandIssue(state, { issueId }) {
        state.timelineExpandedIssues = {
          ...state.timelineExpandedIssues,
          [issueId]: true
        }
      },
      showError(state, msg) {
        state.messages = {...state.messages, error: msg }
      },
      showSuccess(state, msg) {
        state.messages = {...state.messages, success: msg }
      }
    },

    getters: {
      // user: state => state.auth.user,
      userNewspapers: state => state.auth.user ? state.auth.user.newspapers : [],
      newspaper: state => id => state.newspapers[id],
      getNewspaperSubscription: state => newspaper => state.subscriptions === null ? false : state.subscriptions.newspapers[newspaper.fullName],
      getAuthorSubscription: state => author => {
        if (state.subscriptions === null) {
          return null
        }
        return state.subscriptions.authors[author.id]
      }
    },

    actions,
    strict: process.env.NODE_ENV !== 'production',
    plugins: [
      analyticsMiddleware
    ]
  })
}

export default createStore
