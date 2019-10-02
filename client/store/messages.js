export const state = () => ({
  error: null,
  success: null,
})


export const mutations = {
  error(state, msg) {
    state.error = msg
  },
  success(state, msg) {
    state.success = msg
  },
  clear(state) {
    state.success = null
    state.error = null
  }
}
