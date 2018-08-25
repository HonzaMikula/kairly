<template>
  <dialog-window :closeModal="closeModal" v-if="!loading">
    <modal-dialog role="dialog" @click.stop class="tutorial">
      <header>
        <h1>Tutorial</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <div>
        <Issue :issue="issue" :subscription="newspaper.subscription" />
      </div>
    </modal-dialog>
  </dialog-window>
</template>


<script>
import { mapActions } from 'vuex'

import Issue from '@/components/IssueWrapper'
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'TutorialModalComponent',

  props: {
    closeModal: Function
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

  methods: mapActions(['getNewspaperDetail']),

  async created() {
    const resp = await getNewspaperDetail({
      newspaperId: 'janmikula/kairly',
      issue: 1
    })
    this.newspaper = resp.newspaper
    this.issue = resp.issue
    this.loading = false
  }
}
</script>

<style lang="sass">
modal-dialog.tutorial
  min-height: 500px
  width: 970px
  grid-template-rows: 1fr

  > div
    padding-top: $baseline
    max-height: 80vh
    overflow: auto

</style>
