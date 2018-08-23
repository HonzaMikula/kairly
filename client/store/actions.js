import * as api from '@/api'

function onError(err, commit) {
  commit('showError', (err + '') || 'Request failed')
  // eslint-disable-next-line no-console
  console.log(err)
}

export const getProfile = async ({ commit }) => {
  try {
    const resp = await api.getProfile()
    const { user } = resp
    commit('user', {
      user,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'User visit',
            eventAction: user.name
          }]
        ]
      }
    })
    commit('backlog', resp.backlog)
    resp.newspapers.forEach(newspaper => commit('newspaperTitle', newspaper))
    commit('managedNewspapers', resp.newspapers.map(n => n.fullName))
    commit('subscriptions', resp.subscriptions)
    return resp
  } catch (err) {
    commit('user', false)
    commit('backlog', {})
    commit('managedNewspapers', [])
    commit('subscriptions', { authors: {}, newspapers: {}})
    const isUnauthorized = err.message == 'Unauthorized' || (err.response && err.response.status === 401)
    if (!isUnauthorized) {
      onError(err, commit)
    }
  }
}

export const logout = () => {
  api.clearToken()
  // fot now rather reload page to clear cache in store
  window.location.reload()
}

export const getNewspapers = ({ commit, state }, newspaperIds) => {
  return Promise.all(
    newspaperIds
      .filter(id => !(id in state.newspapers))
      .map(id =>
        api.getNewspaperDetail(id)
          .then(resp => {
            const { newspaper } = resp
            commit('newspaper', newspaper)
            return newspaper
          })
          .catch(err => onError(err, commit))
      )
  )
}

export const subscribe = async ({ commit }, fullName) => {
  commit('invalidateTimeline')
  try {
    const newspaper = await api.subscribeNewspaper(fullName)
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

export const unsubscribe = async ({ commit }, fullName) => {
  commit('invalidateTimeline')
  try {
    const newspaper = await api.unsubscribeNewspaper(fullName)
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

export const subscribeAuthor = async ({ commit }, { authorId, periodicity }) => {
  commit('invalidateTimeline')
  try {
    await api.subscribeAuthor(authorId, periodicity)
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

export const unsubscribeAuthor = async ({ commit }, { authorId }) => {
  commit('invalidateTimeline')
  try {
    await api.unsubscribeAuthor(authorId)
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

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', newspaper)
}

export const loadMoreTimeline = async ({ commit, state }) => {
  commit('timelineRequested')
  try {
    const timeline = await api.getTimeline(state.timeline.cursor)
    commit('timelineReceived', timeline)
    return timeline
  } catch (err) {
    onError(err, commit)
  }
}

export const invalidateTimeline = ({ commit }) => {
  commit('invalidateTimeline')
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

export const startNewspaper = async ({ commit }, { authorId, newspaper: newspaperData }) => {
  try {
    const newspaper = await api.createNewspaper(authorId, newspaperData)
    commit('newspaper', newspaper)
    commit('appendManagedNewspaper', {
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

export const updateNewspaper = async ({ commit }, { fullName, fields }) => {
  try {
    const newspaper = await api.updateNewspaper(fullName, fields)
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

export const deleteNewspaper = async ({ commit }, newspaper) => {
  try {
    await api.deleteNewspaper(newspaper.fullName)
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

export const addToBacklog = async ({ commit }, { newspaper, post }) => {
  try {
    // TODO to have better user experience, post can be added immediately
    // and reverted when api call fails
    await api.addToBacklog(newspaper.fullName, post.id)
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

export const removeFromBacklog = async ({ commit }, { newspaper, post }) => {
  try {
    // TODO to have better user experience, post can be removed immediately
    // and reverted when api call fails
    await api.deleteFromBacklog(newspaper.fullName, post.id)
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
