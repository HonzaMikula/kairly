import * as api from '@/api'

function createErrorHadler(commit) {
  return err => {
    commit('showError', (err + '') || 'Request failed')
    // eslint-disable-next-line no-console
    console.log(err)
    return err
  }
}

export const getProfile = ({ commit }) => {
  return api
    .getProfile()
    .then(
      resp => {
        commit('user', resp.user)
        commit('backlog', resp.backlog)
        resp.newspapers.forEach(newspaper => commit('newspaper', newspaper))
        commit('managedNewspapers', resp.newspapers.map(n => n.fullName))
        commit('subscriptions', resp.subscriptions)
        return resp
      },
      err => {
        commit('user', false)
        commit('backlog', {})
        commit('managedNewspapers', [])
        commit('subscriptions', { authors: {}, newspapers: {}})
        if (err.status !== 401) {
          createErrorHadler(commit)(err)
        }
      }
    )
}

export const logout = () => {
  api.clearToken()
  // fot now rather reload page to clear cache in store
  window.location.reload()
}

export const getNewspapers = ({ commit, state }, newspaperIds) => {
  return Promise.all(
    newspaperIds
      // HACK: check for periodicity => newspaper is fully loaded (not just name and title), TODO do not save partialy loaded into store
      .filter(id => !(id in state.newspapers && state.newspapers.periodicity))
      .map(id =>
        api.getNewspaperDetail(id)
          .then(resp => {
            const { newspaper } = resp
            commit('newspaper', newspaper)
            return newspaper
          })
          .catch(createErrorHadler(commit))
      )
  )
}

export const subscribe = ({ commit }, fullName) => {
  commit('invalidateTimeline')
  return api.subscribeNewspaper(fullName).then(newspaper => {
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
  })
  .catch(createErrorHadler(commit))
}

export const unsubscribe = ({ commit }, fullName) => {
  commit('invalidateTimeline')
  return api.unsubscribeNewspaper(fullName).then(newspaper => {
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
  })
  .catch(createErrorHadler(commit))
}

export const subscribeAuthor = ({ commit }, { authorId, periodicity }) => {
  commit('invalidateTimeline')
  return api.subscribeAuthor(authorId, periodicity).then(() => {
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
  })
}

export const unsubscribeAuthor = ({ commit }, { authorId }) => {
  commit('invalidateTimeline')
  return api.unsubscribeAuthor(authorId).then(() => {
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
  })
}

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', newspaper)
}

export const loadMoreTimeline = ({ commit, state }) => {
  commit('timelineRequested')
  return api
    .getTimeline(state.timeline.cursor)
    .then(timeline => {
      commit('timelineReceived', timeline)
      return timeline
    })
    .catch(createErrorHadler(commit))
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

export const startNewEdtion = ({ commit }, { authorId, newspaper }) => {
  return api.createNewspaper(authorId, newspaper)
  .then(resp => {
    const { newspaper } = resp
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
  })
  .catch(createErrorHadler(commit))
}

export const updateEdtion = ({ commit }, { fullName, fields }) => {
  return api.updateNewspaper(fullName, fields)
  .then(resp => {
    const { newspaper } = resp
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
  })
  .catch(createErrorHadler(commit))
}



export const deleteNewspaper = ({ commit }, newspaper) => {
  return api.deleteNewspaper(newspaper.fullName)
  .then(() => {
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
  })
  .catch(createErrorHadler(commit))
}

export const addToBacklog = ({ commit }, { newspaper, post }) => {
  return api.addToBacklog(newspaper.fullName, post.id)
  // TODO to have better user experience, post can be added immediately
  // and reverted when api call fails
  .then(() => {
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
  })
  .catch(createErrorHadler(commit))
}

export const removeFromBacklog = ({ commit }, { newspaper, post }) => {
  return api.deleteFromBacklog(newspaper.fullName, post.id)
  // TODO to have better user experience, post can be removed immediately
  // and reverted when api call fails
  .then(() => {
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
  })
  .catch(createErrorHadler(commit))
}
