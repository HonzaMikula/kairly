<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="100"
  >
    <Welcome v-if="!loading && issues.length === 0"/>

    <IssueWrapper v-for="issue in issues"
      :key="issue.id"
      :issue="issue"
      :isSubscribed="true" />

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

  data: function () {
    return {
      'loading': true,
      'cursor': null,
      'issues': []
    }
  },

  components: {
    IssueWrapper,
    Welcome,
  },

  computed: {
    ...mapState({
      editions: state => state.editions || []
    })
  },

  methods: {
    handleTimelineData: function(timeline) {
      timeline.issues.forEach(issue => this.issues.push(issue))
      this.cursor = timeline.cursor
      this.loading = false
    },

    loadMore: function() {
      if (this.cursor) {
        this.loading = true
        api.getTimeline(this.cursor).then(this.handleTimelineData)
      }
    }
  },

  created() {
    if (this.editions === []) {
      this.issues = []
      this.loading = false
    } else {
      api.getTimeline().then(this.handleTimelineData)
    }
  }
}
</script>
