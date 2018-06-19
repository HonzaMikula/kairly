import * as api from '@/api'

import router from '@/router'

export const getProfile = ({ commit }) => {
  api
    .getProfile()
    .then(
      resp => {
        commit('user', resp.user)
        commit('managedAuthors', resp.authors),
        commit('managedEditions', resp.editions)

      },
      () => {
        commit('user', false)
        commit('managedAuthors', [])
        commit('managedEditions', [])
      }
    )
}

export const logout = ({ commit }) => {
  api.clearToken()
  commit('user', false)
}

export const getEditions = ({ commit, state }) => {
  if (!state.allEditionsLoaded) {
    api
      .getEditions()
      .then(
        editions => commit('allEditions', editions),
        () => commit('allEditions', null)
      )
  }
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
