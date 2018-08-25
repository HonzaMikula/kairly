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
      issues: state => state.timeline.issues,
      loading: state => state.timeline.loading,
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

    // TODO load when needed (user opens dropdown) or better
    // on background after component is displayed
    await store.dispatch('getUserBacklog')

    // TODO nice to have fetch new data when timeline is too old
    const { timeline } = store.state
    if (!timeline.loading && timeline.issues === null) {
      await store.dispatch('loadTimeline')
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
