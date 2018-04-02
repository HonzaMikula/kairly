<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loadDisabled"
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
    loadDisabled() {
      return this.loading || !this.hasMore
    },

    ...mapState({
      issues: state => state.timeline.issues,
      loading: state => state.timeline.loading,
      hasMore: state => !!state.timeline.cursor,
      expandedIssues: state => state.timeline.expandedIssues
    })
  },

  methods: {
    loadMore() {
      this.$store.dispatch('loadMoreTimeline')
    }
  },

  created() {
    if (!this.loading && this.issues === null) {
      this.$store.dispatch('loadMoreTimeline')
    }
  }
}
</script>

<style lang="sass">
timeline-view 
  display: block
  padding: $baseline
  margin: 0 auto
  width: 900px

  @media (max-width: $mobile)
    padding: $baseline 0
    width: $mobile
</style>
