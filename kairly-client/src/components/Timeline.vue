<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="100"
    v-keep-scroll
  >
    <Welcome v-if="!loading && issues.length === 0"/>

    <IssueWrapper v-for="issue in issues"
      :key="issue.id"
      :issue="issue"
      :isSubscribed="true"
      :expanded="expandedIssues[issue.id]" />

    <loading-spinner v-if="loading"></loading-spinner>
  </timeline-view>
</template>

<script>
import * as api from '@/api'
import { mapState } from 'vuex'

import IssueWrapper from '@/components/IssueWrapper'
import Welcome from '@/components/Welcome'

export default {
  name: 'Timeline',

  components: {
    IssueWrapper,
    Welcome,
  },

  computed: {
    ...mapState({
      issues: state => state.timeline.issues,
      loading: state => state.timeline.loading,
      expandedIssues: state => state.timeline.expandedIssues
    })
  },

  methods: {
    loadMore() {
      this.$store.dispatch('loadMoreTimeline')
    }
  },

  created() {
    if (!loading && !issues.length) {
      this.$store.dispatch('loadMoreTimeline')
    }
  }
}
</script>
