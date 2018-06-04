<template>
  <issue-detail-view>
    <div v-if="!loading">
      <Issue :issue="issue" :subscription="edition.subscription" />
    </div>
  </issue-detail-view>
</template>


<script>
import * as api from '@/api'

import Issue from '@/components/IssueWrapper'


export default {
  name: 'EditionDetail',

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
