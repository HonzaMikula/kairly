import Vue from 'vue'

export const state = () => ({
  today: null,
  hasNoActiveSubscriptions: false,
  expandedIssues: {},
  timeline: {
    // of date : [ issues ]
  },
})

export const actions = {
  async load({ commit, state }, { endpoint='/timeline', date, cachedOnly=false}) {
    let cacheKey
    if (endpoint === '/timeline') {
      cacheKey = date
      // TODO check not only valid to but also change of hour or too old timeline
      // but this is not important now
      if (!cacheKey && state.today && state.today.validTo > (Date.now() / 1000)) {
        // if today is requested (no date arg) then lookup to helper structure which
        // keeps current value of "today" (mind that "today" may not match real today)
        cacheKey = state.today.date
      }
    } else {
      cacheKey = endpoint
    }

    if (state.timeline[cacheKey]) {
      return state.timeline[cacheKey]
    }

    if (cachedOnly) {
      return null
    }

    const { status, data } = await this.$axios.get(endpoint, {params: {date}})

    if (status === 204) {
      commit('hasNoActiveSubscriptions')
      return null
    }

    // group recommendations
    data.issues.forEach(issue => {
      const posts = []
      const recommendedPosts = []
      const recommendedIssues = []
      issue.posts.forEach(log => {
        if (log.post.type === 'recommendation-post') {
          recommendedPosts.push(log.post)
        } else if (log.post.type === 'recommendation-issue') {
          recommendedIssues.push(log.post)
        } else {
          posts.push(log)
        }
      })
      if (recommendedPosts.length || recommendedIssues.length) {
        const sample = recommendedPosts.length ? recommendedPosts[0] : recommendedIssues[0]
        posts.push({
          post: {
            author: sample.author,
            id: `wrapper-${sample.id}`,
            type: 'recommendations',
            posts: recommendedPosts,
            issues: recommendedIssues,
          },
          editorial: null
        })
        issue.posts = posts
      }
    })

    if (data.recommended) {
      data.recommended.forEach(id => commit('recommendedIssue', {id, value: true}))
    }

    if (endpoint === '/timeline' && !date) {
      commit('today', {date: data.date, validTo: data.validTo})
    }

    commit('received', data)
    return data
  },

  expandIssue({ commit }, issueId) {
    commit('expandIssue', { issueId })

    this.$ga.event({
      eventCategory: 'Show more (issue)',
      eventAction: issueId
    })
  }

}

export const mutations = {
  resetState(state) {
    state.today = null
    state.hasNoActiveSubscriptions = false
    state.expandedIssues = {}
    state.timeline = {}
  },
  invalidate(state) {
    state.hasNoActiveSubscriptions = false
    state.timeline = {}
  },
  received(state, { date, issues, links }) {
    Vue.set(state.timeline, date, { issues, links })
  },
  hasNoActiveSubscriptions(state) {
    state.hasNoActiveSubscriptions = true
  },
  today(state, value) {
    state.today = value
  },
  expandIssue(state, { issueId }) {
    state.expandedIssues = {
      ...state.expandedIssues,
      [issueId]: true
    }
  },
}
