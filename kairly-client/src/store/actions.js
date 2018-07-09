import * as api from '@/api'

function createErrorHadler(commit) {
  return err => {
    commit('showError', (err + '') || 'Request failed')
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
        return resp
      },
      err => {
        commit('user', false)
        commit('backlog', {})
        commit('managedEditions', [])
        createErrorHadler(commit)(err)
      }
    )
}

export const logout = ({ commit }) => {
  api.clearToken()
  commit('user', false)
  commit('backlog', {})
  commit('managedEditions', [])
  // fot now rather reload page to clear cache in store
  window.location.reload()
}

export const getUserEditions = ({ commit }) => {
  return api
    .getUserEditions()
    .then(
      editions => {
        editions.forEach(edition => commit('edition', edition))
        commit('subscribedEditions', editions.map(e => e.fullName))
        return editions
      }
    )
    .catch(createErrorHadler(commit))
}

export const getEditions = ({ commit, state }, editionIds) => {
  return Promise.all(
    editionIds
      .filter(id => !(id in state.editions))
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

export const subscribe = ({ commit }, { edition, value}) => {
  commit('invalidateTimeline')
  let p
  if (value) {
    p = api.subscribeEdition(edition.fullName)
  } else {
    p = api.unsubscribeEdition(edition.fullName)
  }
  return p.then(edition => {
    commit('edition', edition)
    return edition
  })
  .catch(createErrorHadler(commit))
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
