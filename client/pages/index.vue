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
              :to="{name: 'timeline-date', params: {date: links.prev}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="links.prev"
            >Previous day</nuxt-link>

            <nuxt-link
              v-if="links.next"
              :to="{name: 'timeline-date', params: {date: links.next}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="links.next"
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
      date: null // date returned from timeline request
    }
  },

  computed: {
    ...mapState({
      noSubscriptions: state => state.timelineHasNoActiveSubscriptions,
      expandedIssues: state => state.timelineExpandedIssues
    }),

    loading() {
      return !this.noSubscriptions && !this.date
    },

    timeSlots() {
      if (this.loading) { return [] }

      const { issues } = this.$store.state.timeline[this.date]
      const timeSlots = []
      let slot = null

      issues.forEach(issue => {
        if (slot === null || slot.time !== issue.time) {
          slot = { time: issue.time, issues: []}
          timeSlots.push(slot)
        }
        slot.issues.push(issue)
      })

      return timeSlots
    },

    links() {
      if (this.loading) { return {} }

      return this.$store.state.timeline[this.date].links
    }
  },

  async fetch ({ store, params, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },

  async created() {
    if (process.client && !this.noSubscriptions) {
      // TODO load timeline and backlog in parallel

      const { date } = this.$route.params

      this.date = await this.$store.dispatch('loadTimeline', date)

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
