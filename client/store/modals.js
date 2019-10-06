
export const state = () => ({
  authorSubscription: null,
  newspaperSubscription: null,
})

export const mutations = {
  authorSubscription(state, author) {
    state.authorSubscription = author
  },

  newspaperSubscription(state, newspaper) {
    state.newspaperSubscription = newspaper
  }
}
