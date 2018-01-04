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

export const login = ({ commit, dispatch }, { username, password }) => {
  api
    .createToken(username, password)
    .then(() => dispatch('getProfile'))
}

export const logout = ({ commit }) => {
  api.clearToken()
  commit('user', false)
}
