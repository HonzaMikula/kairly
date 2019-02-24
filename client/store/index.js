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
      today: null,
      timelineHasNoActiveSubscriptions: false,
      timelineExpandedIssues: {},
      timeline: {
        // of date : [ issues ]
      },
      messages: {
        error: null,
        success: null,
      },
      locale: null
    },

    mutations: {
      resetState(state) {
          state.subscriptions = null
          state.backlog = null
          state.newspapers = {}
          state.authors = {}
          state.today = null
          state.timelineHasNoActiveSubscriptions = false
          state.timelineExpandedIssues = {}
          state.timeline = {}
      },

      updateCredits(state, credits) {
        state.auth.user.credits = credits
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
      newspaperSubscription(state, {subscription, fullName}) {
        if (state.subscriptions) {
          if (subscription) {
            state.subscriptions = {
              ...state.subscriptions,
              newspapers: {...state.subscriptions.newspapers, ...subscription}
            }
          } else {
              Vue.delete(state.subscriptions.newspapers, fullName)
          }
        }
      },
      authorSubscription(state, { subscription, authorId}) {
        if (state.subscriptions) {
          if (subscription) {
            state.subscriptions = {
              ...state.subscriptions,
              authors: {...state.subscriptions.authors, ...subscription}
            }
          } else {
              Vue.delete(state.subscriptions.authors, authorId)
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
      timelineReceived(state, { date, issues, links }) {
        Vue.set(state.timeline, date, { issues, links })
      },
      timelineHasNoActiveSubscriptions(state) {
        state.timelineHasNoActiveSubscriptions = true
      },
      today(state, value) {
        state.today = value
      },
      invalidateTimeline(state) {
        state.timelineHasNoActiveSubscriptions = false
        state.timeline = {}
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
      },
      setLang (state, locale) {
        state.locale = locale
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
      },
      monthSpending: state => {
        if (!state.subscriptions) return null
        let cents = 0
        Object.entries(state.subscriptions.newspapers).forEach(([fullName, s]) => {
          const newspaper = state.newspapers[fullName]
          cents += Math.round(parseFloat(newspaper.price) * 100)
          if (s.donation) {
            cents += Math.round(parseFloat(s.donation) * 100)
          }
        })
        Object.values(state.subscriptions.authors).forEach(s => {
          cents += Math.round(parseFloat(s.author.price) * 100)
          if (s.donation) {
            cents += Math.round(parseFloat(s.donation) * 100)
          }
        })
        const mod = cents % 100
        return ~~(cents / 100) + "." + (mod < 10 ? "0" : "") + mod
      },
      hasSuspendedSubscription: state => {
        if (!state.subscriptions) {
          return false
        }
        return !!(
          Object.values(state.subscriptions.newspapers).find(s => s.state === 'suspended') ||
          Object.values(state.subscriptions.authors).find(s => s.state === 'suspended')
        )
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
