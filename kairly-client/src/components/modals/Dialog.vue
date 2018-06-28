<template>
  <modal-window @click="closeModal()">
    <slot></slot>
  </modal-window>
</template>

<script>

export default {
  name: 'DialogWindowComponent',

  props: {
    'onClose': Function
  },

  methods: {
    closeModal() {
      this.onClose()
    }
  }
}
</script>

<style lang="sass">
modal-window
  position: fixed
  top: 0
  left: 0

  display: flex
  align-items: center
  justify-content: center
  height: 100%
  width: 100%

  background: rgba(0, 0, 0, 0.1)
  backdrop-filter: blur(5px)

</style>
