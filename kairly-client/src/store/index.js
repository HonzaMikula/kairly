import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    editions: {},
    allEditionsLoaded: false
  },
  mutations: {
    user (state, user) {
      state.user = user
    },
    allEditions (state, editions) {
      editions.forEach(edition => {
        state.editions[edition.id] = edition
      })
      state.allEditionsLoaded = true
    },
    edition (state, edition) {
      state.editions = {...state.editions, [edition.id]: edition}
    }
  },
  getters: {
    loadingUser: state => state.user === null, // Unauthorized -> user === false
    allEditions: state => state.allEditionsLoaded ? Object.values(state.editions) : null,
    edition: state => id => state.editions[id],
  },
  actions,
  strict: process.env.NODE_ENV !== 'production'
})
