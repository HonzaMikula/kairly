import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    editions: null,
  },
  mutations: {
    user (state, user) {
      state.user = user
    },
    editions (state, editions) {
      state.editions = editions
    },
    edition (state, edition) {
      if (state.editions === null) return
      const i = state.editions.findIndex(item => item.id === edition.id)
      if (i !== -1) {
        state.editions.splice(i, 1, edition) // call splice to trigger update
      }
    }
  },
  getters: {
    loadingUser: state => state.user === null // Unauthorized -> user === false
  },
  actions,
  strict: process.env.NODE_ENV !== 'production'
})
