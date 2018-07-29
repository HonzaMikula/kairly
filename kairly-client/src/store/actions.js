import * as api from '@/api'

function createErrorHadler(commit) {
  return err => {
    commit('showError', (err + '') || 'Request failed')
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
        resp.editions.forEach(edition => commit('edition', edition))
        commit('managedEditions', resp.editions.map(e => e.fullName))
        commit('subscriptions', resp.subscriptions)
        return resp
      },
      err => {
        commit('user', false)
        commit('backlog', {})
        commit('managedEditions', [])
        commit('subscriptions', { authors: {}, editions: {}})
        if (err.status !== 401) {
          createErrorHadler(commit)(err)
        }
      }
    )
}

export const logout = ({ commit }) => {
  api.clearToken()
  // fot now rather reload page to clear cache in store
  window.location.reload()
}

export const getEditions = ({ commit, state }, editionIds) => {
  return Promise.all(
    editionIds
      // HACK: check for periodicity => edition is fully loaded (not just name and title), TODO do not save partialy loaded into store
      .filter(id => !(id in state.editions && state.editions.periodicity))
      .map(id =>
        api.getEditionDetail(id)
          .then(resp => {
            const { edition } = resp
            commit('edition', edition)
            return edition
          })
          .catch(createErrorHadler(commit))
      )
  )
}

export const subscribe = ({ commit }, fullName) => {
  commit('invalidateTimeline')
  return api.subscribeEdition(fullName).then(edition => {
    commit('edition', edition)
    commit('addEditionSubscription', fullName)
    return edition
  })
  .catch(createErrorHadler(commit))
}

export const unsubscribe = ({ commit }, fullName) => {
  commit('invalidateTimeline')
  return api.unsubscribeEdition(fullName).then(edition => {
    commit('edition', edition)
    commit('removeEditionSubscription', fullName)
    return edition
  })
  .catch(createErrorHadler(commit))
}

export const subscribeAuthor = ({ commit }, { authorId, periodicity }) => {
  commit('invalidateTimeline')
  return api.subscribeAuthor(authorId, periodicity).then(author => {
    commit('addAuthorSubscription', { authorId, periodicity })
  })
}

export const unsubscribeAuthor = ({ commit }, { authorId }) => {
  commit('invalidateTimeline')
  return api.unsubscribeAuthor(authorId).then(author => {
    commit('removeAuthorSubscription', { authorId })
  })
}

export const editionUpdated = ({ commit }, edition) => {
  commit('edition', edition)
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
  commit('expandIssue', issueId)
}

export const startNewEdtion = ({ commit }, { authorId, edition }) => {
  return api.createEdition(authorId, edition)
  .then(resp => {
    const { edition } = resp
    commit('edition', edition)
    commit('appendManagedEdition', edition.fullName)
    return edition
  })
  .catch(createErrorHadler(commit))
}

export const updateEdtion = ({ commit }, { fullName, fields }) => {
  return api.updateEdition(fullName, fields)
  .then(resp => {
    const { edition } = resp
    commit('edition', edition)
    return edition
  })
  .catch(createErrorHadler(commit))
}



export const deleteEdition = ({ commit }, edition) => {
  return api.deleteEdition(edition.fullName)
  .then(() => {
    commit('removeEdition', edition.fullName)
  })
  .catch(createErrorHadler(commit))
}

export const addToBacklog = ({ commit }, { edition, post }) => {
  return api.addToBacklog(edition.fullName, post.id)
  // TODO to have better user experience, post can be added immediately
  // and reverted when api call fails
  .then(() => {
    commit('backlogAdd', { editionId: edition.fullName, postId: post.id })
  })
  .catch(createErrorHadler(commit))
}

export const removeFromBacklog = ({ commit }, { edition, post }) => {
  return api.deleteFromBacklog(edition.fullName, post.id)
  // TODO to have better user experience, post can be removed immediately
  // and reverted when api call fails
  .then(() => {
    commit('backlogRemove', { editionId: edition.fullName, postId: post.id })
  })
  .catch(createErrorHadler(commit))
}
