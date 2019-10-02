export default {
  methods: {
    handleError(err) {
      if (err.response && err.response.status >= 400) {
        this.$store.commit('messages/error', err.response.data.error)
      } else {
        if (!err.response) {
          // probably dev error
          console.error(err)
        }
        const msg = (err + '') || 'Request failed'
        this.$store.commit('messages/error', msg)
      }
    }
  }
}
