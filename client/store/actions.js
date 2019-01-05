

// function onError(err, commit) {
//   commit('showError', (err + '') || 'Request failed')
//   // eslint-disable-next-line no-console
//   console.log(err)
// }


export async function getUserBacklog({ commit, state }) {
  if (state.backlog) {
    return state.backlog
  }
  const { backlog } = await this.$axios.$get('/backlog')
  commit('backlog', backlog)
  return backlog
}

export async function getSubscriptions({ commit, state }) {
  if (state.subscriptions) {
    return state.subscriptions
  }
  const { newspapers, subscriptions } = await this.$axios.$get('/subscriptions')
  newspapers.forEach(newspaper => commit('newspaper', { newspaper }))
  commit('subscriptions', subscriptions)
  return subscriptions
}

export async function loadTimeline({ commit, state }, { date, cachedOnly=false}) {

  let cacheKey = date
  // TODO check not only valid to but also change of hour or too old timeline
  // but this is not important now
  if (!cacheKey && state.today && state.today.validTo > (Date.now() / 1000)) {
    // if today is requested (no date arg) then lookup to helper structure which
    // keeps current value of "today" (mind that "today" may not match real today)
    cacheKey = state.today.date
  }

  if (state.timeline[cacheKey]) {
    return cacheKey
  }

  if (cachedOnly) {
    return null
  }

  const { status, data } = await this.$axios.get('/timeline', {params: {date}})

  if (status === 204) {
    commit('timelineHasNoActiveSubscriptions')
    return null
  }

  if (!date) {
    commit('today', {date: data.date, validTo: data.validTo})
  }
  commit('timelineReceived', data)
  return data.date
}

export const invalidateTimeline = ({ commit }) => {
  commit('invalidateTimeline')
}

export async function getNewspaperDetail({ commit }, { newspaperId, issue }) {
  const data = await this.$axios.$get(`/newspapers/${newspaperId}`, { params: {issue} })
  commit('newspaper', { newspaper: data.newspaper })
  return data
}

export async function getNewspapers(store, newspaperIds) {
  const missing = newspaperIds.filter(id => !(id in store.state.newspapers))
  if (missing.length) {
    const promises = missing.map(id => getNewspaperDetail.call(this, store, { newspaperId: id }))
    await Promise.all(promises)
  }
  return newspaperIds.map(id => store.state.newspapers[id])
}

export async function getAuthor({ commit, state, dispatch }, authorId) {
  const data = await this.$axios.$get(`/authors/${authorId}`)
  data.newspapers.forEach(n => dispatch('newspaperUpdated', n))
  return data
}

export async function subscribeNewspaper({ commit }, { fullName, donation }) {
  commit('invalidateTimeline')

  const body = {
    donation
  }
  const { subscription } = await this.$axios.$post(`/newspapers/${fullName}/subscription`, body)
  //commit('newspaper', { newspaper })
  commit('newspaperSubscription', {
    fullName,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe newspaper',
          eventAction: fullName
        }]
      ]
    }
  })
  return subscription
}

export async function unsubscribeNewspaper({ commit }, { fullName }) {
  commit('invalidateTimeline')

  const { subscription } = await this.$axios.$delete(`/newspapers/${fullName}/subscription`)
  commit('newspaperSubscription', {
    fullName,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Unsubscribe newspaper',
          eventAction: fullName
        }]
      ]
    }
  })
  return subscription
}

export async function subscribeAuthor({ commit }, { author, donation, periodicity, keepStatus=false }) {
  commit('invalidateTimeline')
  const body = { periodicity, donation }
  if (keepStatus) {
    // use when wanted to keep subscption in canceled status but edit just periodicity
    body.keepStatus = true
  }
  const { subscription, credits } = await this.$axios.$post(`/authors/${author.id}/subscription`, body)
  commit('updateCredits', credits)
  commit('authorSubscription', {
    authorId: author.id,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe author',
          eventAction: periodicity ? periodicity.frequency : 'renewal',
          eventLabel: author.id
        }]
      ]
    }
  })
  return subscription
}

export async function unsubscribeAuthor({ commit }, { author }) {
  commit('invalidateTimeline')

  const { subscription } = await this.$axios.$delete(`/authors/${author.id}/subscription`)
  commit('authorSubscription', {
    authorId: author.id,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe author',
          eventAction: author.id
        }]
      ]
    }
  })
  return subscription
}

export async function startNewspaper({ commit }, { authorId, newspaper: postData }) {
  const { newspaper } = await this.$axios.$post(`/authors/${authorId}/start-newspaper`, postData)
  commit('newspaper', { newspaper })
  commit('appendOwnedNewspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Start newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
  return newspaper
}

export async function updateNewspaper({ commit }, { fullName, fields }) {
  const { newspaper } = await this.$axios.$patch(`/newspapers/${fullName}`, fields)
  commit('newspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Update newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
  return newspaper
}

export async function deleteNewspaper({ commit }, newspaper) {
  await this.$axios.delete(`/newspapers/${newspaper.fullName}`)
  commit('removeNewspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Delete newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export async function addToBacklog({ commit }, { newspaper, post }) {
  // TODO to have better user experience, post can be added immediately
  // and reverted when api call fails
  await this.$axios.put(`/newspapers/${newspaper.fullName}/backlog`, {post: post.id})
  commit('backlogAdd', {
    newspaperId: newspaper.fullName,
    postId: post.id,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Consider for newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export async function removeFromBacklog({ commit }, { newspaper, post }) {
  // TODO to have better user experience, post can be removed immediately
  // and reverted when api call fails
  await this.$axios.delete(`/newspapers/${newspaper.fullName}/backlog`, { data: {post: post.id}})
  commit('backlogRemove', {
    newspaperId: newspaper.fullName,
    postId: post.id,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Stop considering for newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', { newspaper })
}

export const expandIssue = ({ commit }, issueId) => {
  commit('expandIssue', {
    issueId,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Show more (issue)',
          eventAction: issueId
        }]
      ]
    }
  })
}

export const afterLogout = ({ commit }) => {
  commit('resetState')
}
