import Vue from 'vue'

import * as actions from './actions'

export const state = () => {
  return {
    subscriptions: null,
    recommendedIssues: {},
    locale: null,
  }
}

export const mutations = {
  resetState(state) {
    state.subscriptions = null
    state.recommendedIssues = {}
  },
  updateCredits(state, credits) {
    state.auth.user.credits = credits
  },
  subscriptions(state, subscriptions) {
    state.subscriptions = subscriptions
  },
  invalidateSubscriptions(state) {
    state.subscriptions = null
  },
  newspaperSubscription(state, {subscription, fullName}) {
    if (state.subscriptions) {
      if (subscription) {
        Vue.set(state.subscriptions.newspapers, fullName, subscription)
      } else {
        Vue.delete(state.subscriptions.newspapers, fullName)
      }
    }
  },
  authorSubscription(state, { subscription, authorId}) {
    if (state.subscriptions) {
      if (subscription) {
        Vue.set(state.subscriptions.authors, authorId, subscription)
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
  },
  recommendedIssue(state, { id, value }) {
    Vue.set(state.recommendedIssues, id, value)
  },
  setLang (state, locale) {
    state.locale = locale
  }
}

export const getters = {
  userNewspapers: state => state.auth.user ? state.auth.user.newspapers : [],
  getNewspaperSubscription: state => newspaper => state.subscriptions === null ? false : state.subscriptions.newspapers[newspaper.fullName],
  getAuthorSubscription: state => author => {
    if (state.subscriptions === null) {
      return null
    }
    return state.subscriptions.authors[author.id] || null
  },
  monthSpending: state => {
    if (!state.subscriptions) {
      return null
    }
    let cents = 0
    Object.entries(state.subscriptions.newspapers).forEach(([fullName, s]) => {
      const newspaper = state.entities.newspapers[fullName]
      cents += Math.round(parseFloat(newspaper.price) * 100)
      if (s.donation) {
        cents += Math.round(parseFloat(s.donation) * 100)
      }
    })
    Object.entries(state.subscriptions.authors).forEach(([id, s]) => {
      const author = state.entities.authors[id]
      cents += Math.round(parseFloat(author.price) * 100)
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
}
