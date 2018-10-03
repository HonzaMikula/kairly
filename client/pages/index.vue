<template>
  <app-layout>
    <timeline-view>
      <Welcome v-if="noSubscriptions"/>
      <template v-else>
        <template v-if="timeSlots.length">
          <template v-for="timeSlot in timeSlots" >
            <jump-menu :datetime="timeSlot.time" :key="timeSlot.time" :timeSlots="timeSlots" />

            <IssueWrapper v-for="issue in timeSlot.issues"
              :key="issue.id"
              :issue="issue"
              :subscription="true"
              :expanded="expandedIssues[issue.id]" />
          </template>

          <div class="timeline--pagination">
            <p>That's it. You read the entire day.</p>

            <nuxt-link
              :to="{name: 'timeline-date', params: {date: prevDay}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="prevDay"
            >Previous day</nuxt-link>

            <nuxt-link
              v-if="nextDay"
              :to="{name: 'timeline-date', params: {date: nextDay}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="nextDay"
            >Next day</nuxt-link>

          </div>
        </template>

        <template v-else-if="!loading">
          Nothing to read for {{ date }}.
        </template>
      </template>

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
      nextDay: null
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
      expandedIssues: state => state.timelineExpandedIssues
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
      // TODO load timeline and backlog in parallel

      //const { timeline } = this.$store.state
      // if (timeline.issues === null) {
      //   this.$store.dispatch('loadTimeline')
      // }

      const { date } = this.$route.params
      await this.loadTimeline(date)

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


//- Pagination
.timeline--pagination
  padding-top: $baseline

  border-top: 3px solid #ddd

  text-align: center

  //- you read the entire day title
  p
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-2


  //- buttons
  a
    display: inline-block
    border-radius: $baseline
    height: $baseline * 1.5
    padding: 0 $baseline
    margin: 0 $baseline/2

    background: $c-base
    color: #fff

    line-height: $baseline * 1.5

    &:hover,
    &:focus
      background: darken($c-base, 10%)



</style>
