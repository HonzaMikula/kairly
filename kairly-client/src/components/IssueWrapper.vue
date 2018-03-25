<template>
  <component
    :is="'issue-' + issue.type"
    :issue="issue"
    :isSubscribed="true"
    :key="issue.id">
  </component> 
</template>

<script>
import issueEdition from '@/components/issues/edition'
import issueAuthor from '@/components/issues/author'

export default {
  name: 'IssueWrapper',
  props: ['issue'],

  components: {
    issueEdition,
    issueAuthor
  },

  created() {
    if (this.issue.period == 'Posts') // Hack till we have issue type from API
      this.issue.type = 'author'
    else
      this.issue.type = 'edition'
  }
}
</script>
