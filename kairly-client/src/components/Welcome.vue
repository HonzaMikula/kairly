<template>
  <timeline-welcome>
    <template v-if="!loading">
      <Issue :issue="issue" :subscription="edition.subscription" />

      <router-link to="/explore">Start with exploring</router-link>
    </template>
  </timeline-welcome>
</template>

<script>
import * as api from '@/api'
import { mapGetters } from 'vuex'

import Issue from '@/components/IssueWrapper'

export default {
  name: 'Welcome',

  components: {
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
  }
}
</script>

<style lang="sass">
//- Welcome Edition
timeline-welcome
  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
