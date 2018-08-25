

function onError(err, commit) {
  commit('showError', (err + '') || 'Request failed')
  // eslint-disable-next-line no-console
  console.log(err)
}


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
  const { subscriptions } = await this.$axios.$get('/subscriptions')
  commit('subscriptions', subscriptions)
  return subscriptions
}

export async function loadTimeline({ commit, state }) {
  commit('timelineRequested')
  //try {
  const { cursor } = state.timeline
  const timeline = await this.$axios.$get('/timeline', {params: {cursor}})
  commit('timelineReceived', timeline)
  return timeline
  // } catch (err) {
  //   onError(err, commit)
  // }
}

export const invalidateTimeline = ({ commit }) => {
  commit('invalidateTimeline')
}

export async function getNewspaperDetail({ commit }, { newspaperId, issue }) {
  const data = await this.$axios.$get(`/newspapers/${newspaperId}`, {params: {issue}})
  commit('newspaper', data.newspaper)
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

// export async function getAuthor({ commit, state }, id) {
//   let author = state.authors[id]
//   if (author) {
//     return author
//   }
//   resp = await api.getAuthor(id)
//   commit('author', author)
//   return author
// }

export async function subscribe({ commit }, fullName) {
  commit('invalidateTimeline')
  try {
    const newspaper = await this.$axios.$post(`/newspapers/${fullName}/subscribe`)
    commit('newspaper', newspaper)
    commit('addNewspaperSubscription', {
      fullName,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Subscribe newspaper',
            eventAction: fullName
          }]
        ]
      }
    })
    return newspaper
  } catch (err) {
    onError(err, commit)
  }
}

export async function unsubscribe({ commit }, fullName) {
  commit('invalidateTimeline')
  try {
    const newspaper = await this.$axios.$post(`/newspapers/${fullName}/unsubscribe`)
    commit('newspaper', newspaper)
    commit('removeNewspaperSubscription', {
      fullName,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Unsubscribe newspaper',
            eventAction: fullName
          }]
        ]
      }
    })
    return newspaper
  } catch (err) {
    onError(err, commit)
  }
}

export async function subscribeAuthor({ commit }, { authorId, periodicity }) {
  commit('invalidateTimeline')
  try {
    await this.$axios.post(`/authors/${authorId}/subscribe`, periodicity)
    commit('addAuthorSubscription', {
      authorId,
      periodicity,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Subscribe author',
            eventAction: periodicity.frequency,
            eventLabel: authorId
          }]
        ]
      }
    })
  } catch (err) {
    onError(err, commit)
  }
}

export async function unsubscribeAuthor({ commit }, { authorId }) {
  commit('invalidateTimeline')
  try {
    await this.$axios.post(`/authors/${authorId}/unsubscribe`)
    commit('removeAuthorSubscription', {
      authorId,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Subscribe author',
            eventAction: authorId
          }]
        ]
      }
    })
  } catch (err) {
    onError(err, commit)
  }
}

export async function startNewspaper({ commit }, { authorId, newspaper: postData }) {
  try {
    const { newspaper } = await this.$axios.$post(`/authors/${authorId}/start-newspaper`, postData)
    commit('newspaper', newspaper)
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
  } catch (err) {
    onError(err, commit)
  }
}

export async function updateNewspaper({ commit }, { fullName, fields }) {
  try {
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
  } catch (err) {
    onError(err, commit)
  }
}

export async function deleteNewspaper({ commit }, newspaper) {
  try {
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
  } catch (err) {
    onError(err, commit)
  }
}

export async function addToBacklog({ commit }, { newspaper, post }) {
  try {
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
  } catch (err) {
    onError(err, commit)
  }
}

export async function removeFromBacklog({ commit }, { newspaper, post }) {
  try {
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
  } catch (err) {
    onError(err, commit)
  }
}

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', newspaper)
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
