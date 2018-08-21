<template>
  <app-layout>
    <issue-detail-view>
      <div v-if="!loading">
        <Issue :issue="issue" :subscription="newspaper.subscription" />
      </div>
    </issue-detail-view>
  </app-layout>
</template>


<script>
import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'


export default {
  name: 'IssueDetail',

  metaInfo() {
      return {
        title: this.newspaper ? `${this.newspaper.title} #${this.issue.number}` : undefined
      }
  },

  components: {
    AppLayout,
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
    const { author, newspaper, issue } = this.$route.params
    api.getNewspaperDetail(`${author}/${newspaper}`, issue).then(resp => {
      this.newspaper = resp.newspaper
      this.issue = resp.issue
      this.loading = false
    })
  }
}
</script>

<style lang="sass">
issue-detail-view
  display: block
  margin: $baseline auto
  max-width: 900px
</style>
