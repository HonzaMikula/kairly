import request from 'superagent'
import * as api from '@/api'

export const getProfile = ({ commit, state }) => {
  api
    .getProfile()
    .then(
      user => commit('user', user),
      () => commit('user', false)
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
  api
    .postSubscription(edition.id, value)
    .then(
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

export const expandIssue = ({ commit }, issueId) => {
  commit('expandIssue', issueId)
}
