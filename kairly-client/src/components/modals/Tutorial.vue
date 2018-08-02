<template>
  <dialog-window :onClose="onClose">
    <modal-dialog role="dialog" @click.stop>
      <div v-if="!loading">
        <Issue :issue="issue" :subscription="newspaper.subscription" />
      </div>
      <button-close tabindex="0" role="button" @click="onClose">Close</button-close>
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
    onClose: Function
  },

  components: {
    DialogWindow,
    Issue
  },

  data() {
    return {
      loading: true,
      newspaper: null,
      issue: null,
    }
  },

  created() {
    api.getNewspaperDetail('janmikula/kairly', 1).then(resp => {
      this.newspaper = resp.newspaper
      this.issue = resp.issue
      this.loading = false
    })
  }
}
</script>

<style lang="sass">
modal-dialog
  grid-template-rows: 1fr

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
