<template>
  <dialog-window :onClose="closeModal">
    <modal-dialog role="dialog">
      <div v-if="!loading">
        <Issue :issue="issue" :subscription="edition.subscription" />
      </div>
      <button-close tabindex="0" role="button" @click="closeModal()">Close</button-close> 
    </modal-dialog>
  </dialog-window>
</template>


<script>
import * as api from '@/api'

import Issue from '@/components/IssueWrapper'
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'TutorialModalComponent',

  props: {
    'onClose': Function
  },

  components: {
    DialogWindow,
    Issue
  },

  data() {
    return {
      loading: true,
      edition: null,
      issue: null,
    }
  },

  created() {
    api.getEditionDetail('janmikula/kairly', 1).then(resp => {
      this.edition = resp.edition
      this.issue = resp.issue
      this.loading = false
    })
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
  position: relative

  display: block
  border-radius: $baseline / 2
  min-height: 500px
  width: 970px

  background: #fff

  > div
    padding-top: $baseline
    max-height: 80vh
    overflow: auto

  //- close button
  button-close
    position: absolute
    top: -$baseline
    right: 0

    text-transform: lowercase
    cursor: pointer

    &::before
      +fa-icon()

      margin-right: $baseline / 4

      content: $fa-var-times

</style>
