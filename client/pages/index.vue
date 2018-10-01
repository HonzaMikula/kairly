<template>
  <app-layout>
    <timeline-view>
      <Welcome v-if="noSubscriptions"/>
      <div v-else>
        <a v-if="nextDay" href="#" @click.prevent="loadTimeline(nextDay)">Show {{ nextDay }}</a>
        <a href="#" @click.prevent="loadTimeline(prevDay)">Show {{ prevDay }}</a>

        <div v-if="timeSlots.length">
          <div v-for="timeSlot in timeSlots">
            <jump-menu :datetime="timeSlot.time" :timeSlots="timeSlots" />

            <IssueWrapper v-for="issue in timeSlot.issues"
              :key="issue.id"
              :issue="issue"
              :subscription="true"
              :expanded="expandedIssues[issue.id]" />

          </div>
        </div>
        <div v-else>
          Nothing to read for {{ date }}.
        </div>
      </div>

      <loading-spinner v-if="loading"></loading-spinner>
    </timeline-view>
  </app-layout>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import Welcome from '@/components/Welcome'
import JumpMenu from '@/components/widgets/JumpMenu'

export default {
  name: 'Timeline',

  components: {
    IssueWrapper,
    Welcome,
    AppLayout,
    JumpMenu
  },

  data() {
    return {
      noSubscriptions: false,
      loading: true,
      timeSlots: [],
      date: null,
      prevDay: null,
      nextDay: null,
      expandedIssues: {}
    }
  },

  computed: {
    // loadDisabled() {
    //   return this.loading || !this.hasMore
    // },

    ...mapState({
      //issues: state => state.timeline.issues || [] ,
      //loading: state => process.server || state.timeline.loading,
      // hasMore: state => !!state.timeline.cursor,
      //expandedIssues: state => state.timeline.expandedIssues
    })
  },

  //methods: mapActions(['loadTimeline']),

  methods: {
    async loadTimeline(date) {
      this.loading = true

      const response = await this.$axios.get('/timeline', {params: {date}})

      if (response.status === 204) {
        this.noSubscriptions = true
        this.loading = false
        return
      }

      date = response.data.date
      const { issues, links } = response.data

      let slot = null
      const timeSlots = []

      issues.forEach(issue => {
        if (slot === null || slot.time !== issue.time) {
          slot = { time: issue.time, issues: []}
          timeSlots.push(slot)
        }
        slot.issues.push(issue)
      })

      this.timeSlots = timeSlots
      this.date = date
      this.prevDay = links.prev
      this.nextDay = links.next
      this.loading = false
    }
  },

  async fetch ({ store, params, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },

  async created() {
    if (process.client) {
      // load timeline and black in parallel

      //const { timeline } = this.$store.state
      // if (timeline.issues === null) {
      //   this.$store.dispatch('loadTimeline')
      // }

      await this.loadTimeline()

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
