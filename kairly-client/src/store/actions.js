import * as api from '@/api'

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
