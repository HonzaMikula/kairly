<template>
  <app-layout>
    <issue-detail-view>
      <div v-if="!loading">
        <Issue :issue="issue" :subscription="edition.subscription" />
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
        title: this.edition ? `${this.edition.title} #${this.issue.number}` : undefined
      }
  },

  components: {
    AppLayout,
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
    const { editionId, issueId } = this.$route.params
    api.getEditionDetail(editionId, issueId).then(resp => {
      this.edition = resp.edition
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
