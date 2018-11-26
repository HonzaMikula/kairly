<template>
  <app-layout>
    <timeline-view v-if="loggedIn">
      <Welcome v-if="noSubscriptions"/>
      <template v-else>
        <template v-if="timeSlots.length">
          <div
            v-if="links.next"
            class="timeline--top-pagination"
          >
            <p>{{date | moment('dddd, MMMM Do YYYY')}}</p>

            <nuxt-link
              :to="{name: 'timeline-date', params: {date: links.prev}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="links.prev"
            >{{ $t('Previous day') }}</nuxt-link>

            <nuxt-link
              v-if="links.next"
              :to="{name: 'timeline-date', params: {date: links.next}}"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="links.next"
            >{{ $t('Next day') }}</nuxt-link>
          </div>

          <template v-for="timeSlot in timeSlots" >
            <jump-menu :datetime="timeSlot.time" :key="timeSlot.time" :timeSlots="timeSlots" />

            <IssueWrapper v-for="issue in timeSlot.issues"
              :key="issue.id"
              :issue="issue"
              :subscription="true"
            />
          </template>
        </template>

        <template v-else-if="!loading">
          <div class="timeline--empty">
            {{ $t('No articles or tweets.') }}
          </div>
        </template>

        <div class="timeline--pagination" v-if="!loading">
          <p>{{ $t("That's it. You read the entire day.") }}</p>

          <nuxt-link
            :to="{name: 'timeline-date', params: {date: links.prev}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="links.prev"
          >{{ $t('Previous day') }}</nuxt-link>

          <nuxt-link
            v-if="links.next"
            :to="{name: 'timeline-date', params: {date: links.next}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="links.next"
          >{{ $t('Next day') }}</nuxt-link>

        </div>
      </template>

      <loading-spinner v-if="loading"></loading-spinner>
    </timeline-view>
    <Homepage v-else/>
  </app-layout>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import Homepage from '@/components/Homepage'
import Welcome from '@/components/Welcome'
import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'

export default {
  name: 'Timeline',

  // Homepage component is displayed when user is not logged
  auth: false,

  components: {
    AppLayout,
    Homepage,
    IssueWrapper,
    JumpMenu,
    Welcome,
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
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

  watch: {
    loggedIn() {
      this.loadTimeline()
    }
  },

  methods: {
    async loadTimeline() {
      if (this.loggedIn && !this.noSubscriptions) {
        // TODO load timeline and backlog in parallel

        const { date } = this.$route.params

        this.date = await this.$store.dispatch('loadTimeline', { date })

        this.$store.dispatch('getUserBacklog')
      }
    }
  },

  async asyncData({ store, params }) {
    const { state } = store
    const { date } = params

    // data.date keeps date returned from timeline request

    if (!state.auth.loggedIn || state.timelineHasNoActiveSubscriptions) {
      return {
        date: null
      }
    }

    /*
      return only if timeline date is already fetched
      we want render page immediately when all data is alredy in store
      to keep scroll position when user is going back

      on the other hand, when data is not available, make fast transtion
      as possible and keep loading wheel dispayed inside page
    */
    return {
      date: await store.dispatch('loadTimeline', { date, cachedOnly: true })
    }
  },

  created() {
    if (process.client && !this.date) {
      this.loadTimeline()
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

//- Empty timeline
.timeline--empty
  display: table
  margin: $baseline*2 auto
  padding: $baseline $baseline*2

  background: #eee
  border: 1px dashed #ccc

  text-align: center


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
    margin: 0 $baseline/2
    width: 140px

    background: $c-base
    color: #fff

    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: darken($c-base, 10%)

    @media (max-width: $mobile)
      margin: 0 $baseline/4
      width: 120px

      font-size: $fs--1

.timeline--top-pagination
  display: flex
  justify-content: center
  padding-bottom: $baseline

  border-bottom: 3px solid #ddd

  text-align: center

  p
    margin: 0 $baseline
    order: 2

    font-family: $ff-serif
    font-size: $fs-2
    line-height: $baseline * 1.5

  //- buttons
  a
    display: inline-block
    border-radius: $baseline
    height: $baseline * 1.5
    margin: 0 $baseline/2
    width: 140px

    background: $c-base
    color: #fff

    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: darken($c-base, 10%)

    &:first-of-type
      order: 1

    &:last-of-type
      order: 3

    @media (max-width: $mobile)
      margin: 0 $baseline/4
      width: 120px

      font-size: $fs--1


</style>
