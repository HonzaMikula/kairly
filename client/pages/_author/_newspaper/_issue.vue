<template>
  <app-layout>
    <issue-detail-view>
      <Issue :issue="issue" :subscription="newspaper.subscription" />
    </issue-detail-view>
  </app-layout>
</template>


<script>
import { mapActions } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'

export default {
  name: 'IssueDetail',

  head() {
      return {
        title: `${this.newspaper.title} #${this.issue.number}`
      }
  },

  components: {
    AppLayout,
    Issue
  },

  async asyncData({ store, params }) {
    const fullName = `${params.author}/${params.newspaper}`

    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }
    
    const { newspaper, issue } = await store.dispatch('getNewspaperDetail', {
      newspaperId: fullName,
      issue: params.issue
    })
    return { newspaper, issue }
  }
}
</script>

<style lang="sass">
issue-detail-view
  display: block
  margin: $baseline auto
  max-width: 900px
</style>
