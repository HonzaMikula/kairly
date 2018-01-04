import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null
  },
  mutations: {
    user (state, user) {
      state.user = user
    }
  },
  getters: {
    loadingUser: state => state.user === null // Unauthorized -> user === false
  },
  actions,
  strict: process.env.NODE_ENV !== 'production'
})
