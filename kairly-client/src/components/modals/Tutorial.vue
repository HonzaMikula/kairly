<template>
  <dialog-window :onClose="closeModal">
    <modal-dialog role="dialog">
      Here will be tutorial/help.

      <button @click="closeModal()">Close</button>
    </modal-dialog>
  </dialog-window>
</template>


<script>

import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'TutorialModalComponent',

  props: {
    'onClose': Function
  },

  components: {
    DialogWindow
  },

  methods: {
    closeModal() {
      this.onClose()
    }
  }
}
</script>

<style lang="sass">
modal-dialog
  display: block
  border-radius: $baseline / 2
  min-height: 500px
  width: 970px

  background: #fff
</style>
