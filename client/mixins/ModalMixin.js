
export default {
  props: {
    active: Boolean,
  },

  methods: {
    closeModal(event) {
      this.$emit('close')
      this.$emit('update:active', false)
    }
  }
}
