<template>
  <app-layout>
    <timeline-view v-if="loggedIn">
      <Welcome v-if="showWelcome"/>

      <template v-else>
        <header
          class="timeline--header"
          v-if="!loading"
        >
          <nuxt-link
            :to="{name: 'timeline-date', params: {date: links.prev}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          ></nuxt-link>

          <nuxt-link
            v-if="links.next"
            :to="{name: 'timeline-date', params: {date: links.next}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="'Next day ('+ links.next +')'"
            :class="['next', {'is-disabled': !links.next}]"
          ></nuxt-link>
        </header>

        <template v-if="timeSlots.length > 0">
          <template v-for="timeSlot in timeSlots">
            <jump-menu :datetime="timeSlot.time" :key="timeSlot.time" :timeSlots="timeSlots" />

            <IssueWrapper v-for="issue in timeSlot.issues"
              :key="issue.id"
              :issue="issue"
              :subscription="true"
            />
          </template>
        </template>

        <div class="timeline--empty" v-else-if="!loading">
          {{ $t('No articles or tweets.') }}
        </div>

        <footer class="timeline--footer" id="start" v-if="!loading">
          <p>{{ $t("That's it. You read the entire day.") }}</p>

          <nuxt-link
            :to="{name: 'timeline-date', params: {date: links.prev}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          ></nuxt-link>

          <nuxt-link
            v-if="links.next"
            :to="{name: 'timeline-date', params: {date: links.next}}"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="'Next day ('+ links.next +')'"
            :class="['next', {'is-disabled': !links.next}]"
          ></nuxt-link>
        </footer>
      </template>

      <loading-spinner v-if="loading"></loading-spinner>
    </timeline-view>

    <Homepage v-else/>
  </app-layout>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import moment from 'moment'

import Homepage from '@/components/Homepage'
import Welcome from '@/components/Welcome'
import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'

export default {
  name: 'Timeline',

  // Homepage component is displayed when user is not logged
  auth: false,

  head() {
    return {
      title: 'Kairly',
      meta: [
        { hid: 'description', name: 'description', content: 'Timeline showing you latest issues of newspapers you subscribed to.' },
      ]
    }
  },

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
      expandedIssues: state => state.timelineExpandedIssues
    }),

    loading() {
      return !this.showWelcome && !this.date
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
    loggedIn(value) {
      if (value) {
        this.loadTimeline()
      } else {
        this.date = null
        this.showWelcome = false
      }
    }
  },

  methods: {
    async loadTimeline() {
      if (this.loggedIn && !this.$store.state.timelineHasNoActiveSubscriptions) {
        // TODO load timeline and backlog in parallel

        const { date } = this.$route.params

        this.date = await this.$store.dispatch('loadTimeline', { date })
        if (this.date === null) {
          this.showWelcome = true
        }

        this.$store.dispatch('getUserBacklog')
      }
    }
  },

  async asyncData({ store, params }) {
    const { state } = store
    const { date } = params

    // data.date keeps date returned from timeline request
    if (!state.auth.loggedIn) {
      return {
        showWelcome: false,
        date: null
      }
    }

    if (state.timelineHasNoActiveSubscriptions) {
      return {
        showWelcome: true, // don't change this when user subscribe on Welcome page
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
      showWelcome: false,
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
  padding: $baseline $baseline 0 $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline/2 0

//- Empty timeline
.timeline--empty
  display: table
  margin: $baseline*2 auto
  padding: $baseline $baseline*2

  background: #eee
  border: 1px dashed #ccc

  text-align: center

//- Header
.timeline--header
  display: flex
  justify-content: space-between

//- Footer
.timeline--footer
  display: flex
  padding-top: $baseline

  border-top: 3px solid #ddd

  text-align: center

  //- you read the entire day title
  p
    flex: 1
    order: 2
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 1.5

//- buttons for switching days
.timeline--footer,
.timeline--header
  a
    display: block
    border-radius: 100%
    height: $baseline * 1.5
    width: $baseline * 1.5

    background: #fff
    color: #000

    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: $c-base
      color: #fff

    &.is-disabled
      opacity: 0.5

      cursor: default

      &:hover,
      &:focus
        background: #fff
        color: #000

    &::before
      +fa-icon()
      @extend .fas

    &.previous
      order: 1

      &::before
        content: fa-content($fa-var-arrow-left)

    &.next
      order: 3

      &::before
        content: fa-content($fa-var-arrow-right)

.timeline--header
  margin-top: 0
  padding-top: 0

  border-top: 0

</style>
