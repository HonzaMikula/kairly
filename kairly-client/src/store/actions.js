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
  if (state.editions == null) {
    api
      .getEditions()
      .then(
        editions => commit('editions', editions),
        () => commit('editions', null)
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
