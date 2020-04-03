
export default {
  props: {
    active: {
      type: Boolean,
      default: true
    }
  },

  methods: {
    closeModal (event) {
      this.$emit('close')
      this.$emit('update:active', false)
    }
  }
}
