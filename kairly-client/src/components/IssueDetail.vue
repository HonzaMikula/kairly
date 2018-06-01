<template>
  <div>
    <div v-if="!loading">
      <Issue :issue="issue" :subscription="edition.subscription" />
    </div>
  </div>
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

</style>
