import * as api from '@/api'

import router from '@/router'

export const getProfile = ({ commit }) => {
  api
    .getProfile()
    .then(
      resp => {
        commit('user', resp.user)
        commit('backlog', resp.backlog)
        commit('managedEditions', resp.editions)

      },
      () => {
        commit('user', false)
        commit('backlog', {})
        commit('managedEditions', [])
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

export const getUserEditions = ({ commit, state }) => {
  api
    .getUserEditions()
    .then(
      editions => {
        editions.forEach(edition => commit('edition', edition))
        commit('subscribedEditions', editions.map(e => e.id))
      }
    )
}

export const getEditions = ({ commit, state }, editionIds) => {
  editionIds.forEach(id => {
    if (!(id in state.editions)) {
      api.getEditionDetail(id).then(resp => commit('edition', resp.edition))
    }
  })
}

export const subscribe = ({ commit }, { edition, value}) => {
  commit('invalidateTimeline')
  let p
  if (value) {
    p = api.subscribeEdition(edition.id)
  } else {
    p = api.unsubscribeEdition(edition.id)
  }
  p.then(
    edition => commit('edition', edition)
  )
}

export const editionUpdated = ({ commit }, edition) => {
  commit('edition', edition)
}

export const loadMoreTimeline = ({ commit, state }) => {
  commit('timelineRequested')
  api
    .getTimeline(state.timeline.cursor)
    .then(timeline => commit('timelineReceived', timeline) )
}

export const invalidateTimeline = ({ commit }) => {
  commit('invalidateTimeline')
}

export const expandIssue = ({ commit }, issueId) => {
  commit('expandIssue', issueId)
}

export const startNewEdtion = ({ commit }, { authorId, edition }) => {
  api.createEdition(authorId, edition)
  .then(resp => {
    const { edition } = resp
    commit('appendManagedEdition', edition)
    // there is problem with push using editionId param, it can't handle
    // parameter which contains /
    //router.push({ name: 'edition', params: { editionId: edition.id }})
    router.push('/editions/' + edition.id )
  })
}

export const deleteEdition = ({ commit }, edition) => {
  api.deleteEdition(edition.id)
  .then(() => {
    commit('removeManagedEdition', edition)
    router.push({ name: 'author', params: { authorId: edition.editor.id }})
  })
}

export const addToBacklog = ({ commit }, { edition, post }) => {
  api.addToBacklog(edition.id, post.id)
  // TODO to have better user experience, post can be added immediately
  // and reverted when api call fails
  .then(() => {
    commit('backlogAdd', { editionId: edition.id, postId: post.id })
  })
}

export const removeFromBacklog = ({ commit }, { edition, post }) => {
  api.deleteFromBacklog(edition.id, post.id)
  // TODO to have better user experience, post can be removed immediately
  // and reverted when api call fails
  .then(() => {
    commit('backlogRemove', { editionId: edition.id, postId: post.id })
  })
}
