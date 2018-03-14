<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="100"
  >
    <Welcome v-if="!loading && issues.length === 0"/>

    <Issue v-for="issue in issues"
      :key="issue.id"
      :issue="issue"
      :isSubscribed="true" />

    <loading-spinner v-if="loading"></loading-spinner>
  </timeline-view>
</template>

<script>
import * as api from '@/api'
import { mapState } from 'vuex'

import Issue from '@/components/Issue'
import Welcome from '@/components/Welcome'

export default {
  name: 'Timeline',

  data: function () {
    return {
      'loading': true,
      'page': 1,
      'lastPage': null,
      'issues': []
    }
  },

  components: {
    Issue,
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
      this.lastPage = timeline.lastPage
      this.loading = false
    },

    loadMore: function() {
      if (this.page < this.lastPage) {
        this.page += 1
        this.loading = true
        api.getTimeline(this.page).then(this.handleTimelineData)
      }
    }
  },

  created() {
    if (this.editions === []) {
      this.issues = []
      this.lastPage = 1
      this.loading = false
    } else {
      api.getTimeline().then(this.handleTimelineData)
    }
  }
}
</script>
