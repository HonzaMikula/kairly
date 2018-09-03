<template>
  <app-layout>
    <timeline-view v-infinite-scroll="loadTimeline"
      infinite-scroll-disabled="loadDisabled"
      infinite-scroll-distance="100"
    >
      <Welcome v-if="!loading && issues.length === 0"/>

      <IssueWrapper v-for="issue in issues"
        :key="issue.id"
        :issue="issue"
        :subscription="true"
        :expanded="expandedIssues[issue.id]" />

      <loading-spinner v-if="loading"></loading-spinner>
    </timeline-view>
  </app-layout>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import Welcome from '@/components/Welcome'

export default {
  name: 'Timeline',

  middleware: ['auth'],

  components: {
    IssueWrapper,
    Welcome,
    AppLayout
  },

  computed: {
    loadDisabled() {
      return this.loading || !this.hasMore
    },

    ...mapState({
      issues: state => state.timeline.issues || [] ,
      loading: state => process.server || state.timeline.loading,
      hasMore: state => !!state.timeline.cursor,
      expandedIssues: state => state.timeline.expandedIssues
    })
  },

  methods: mapActions(['loadTimeline']),

  async fetch ({ store, params, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },

  created() {
    if (process.client) {
      // load timeline and black in parallel

      const { timeline } = this.$store.state
      if (timeline.issues === null) {
        this.$store.dispatch('loadTimeline')
      }
      this.$store.dispatch('getUserBacklog')
    }
  }
}
</script>

<style lang="sass">
timeline-view
  display: block
  padding: $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline 0
</style>
