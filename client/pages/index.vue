<template>
  <AppLayout>
    <div v-if="loggedIn" class="timeline-view">
      <WelcomePage v-if="showWelcome" />

      <TimelineLoader v-else-if="loading" />

      <template v-else>
        <header
          class="timeline--header"
        >
          <nuxt-link
            v-b-tooltip
            :to="{name: 'timeline-date', params: {date: links.prev}}"
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          />

          <nuxt-link
            v-if="links.next"
            v-b-tooltip
            :to="{name: 'timeline-date', params: {date: links.next}}"
            :title="'Next day ('+ links.next +')'"
            :class="['next', {'is-disabled': !links.next}]"
          />
        </header>

        <template v-if="timeSlots.length > 0">
          <template v-for="timeSlot in timeSlots">
            <JumpMenu
              :key="timeSlot.time"
              :datetime="timeSlot.time"
              :time-slots="timeSlots"
            />

            <IssueWrapper
              v-for="issue in timeSlot.issues"
              :key="issue.id"
              :issue="issue"
              :subscription="true"
            />
          </template>
        </template>

        <template v-else>
          <div class="timeline-time-slot">
            <h1>{{ dayTitle }}</h1>
          </div>

          <div class="timeline--empty">
            <h2>{{ $t('No articles or tweets yet') }}</h2>
            <p>
              {{ $t('Nothing was published for you yet. Check your subscriptions or explore more newspapers and authors.') }}
            </p>

            <nuxt-link to="/subscription">{{ $t('Subscriptions') }}</nuxt-link>
            <nuxt-link to="/explore">{{ $t('Explore') }}</nuxt-link>
          </div>
        </template>

        <footer
          id="start"
          class="timeline--footer"
        >
          <p>{{ $t("That's it. You read the entire day.") }}</p>

          <nuxt-link
            v-b-tooltip
            :to="{name: 'timeline-date', params: {date: links.prev}}"
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          />

          <nuxt-link
            v-if="links.next"
            v-b-tooltip
            :to="{name: 'timeline-date', params: {date: links.next}}"
            :title="'Next day ('+ links.next +')'"
            :class="['next', {'is-disabled': !links.next}]"
          />
        </footer>
      </template>
    </div>

    <HomePage v-else />
  </AppLayout>
</template>

<script>
import Vue from 'vue'
import { mapGetters, mapState } from 'vuex'
import moment from 'moment'

import HomePage from '@/components/HomePage'
import WelcomePage from '@/components/WelcomePage'
import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'
import TimelineLoader from '@/components/widgets/TimelineLoader'

export default {
  name: 'Timeline',

  // Homepage component is displayed when user is not logged
  auth: false,

  components: {
    AppLayout,
    HomePage,
    IssueWrapper,
    JumpMenu,
    WelcomePage,
    TimelineLoader
  },

  async asyncData ({ store, params }) {
    const { state } = store
    const { date } = params

    // data.date keeps date returned from timeline request
    if (!state.auth.loggedIn) {
      return {
        showWelcome: false,
        date: null,
        timeline: null
      }
    }

    if (state.timeline.hasNoActiveSubscriptions) {
      return {
        showWelcome: true, // don't change this when user subscribe on Welcome page
        date: null,
        timeline: null
      }
    }

    /*
      return only if timeline date is already fetched
      we want render page immediately when all data is alredy in store
      to keep scroll position when user is going back

      on the other hand, when data is not available, make fast transtion
      as possible and keep loading wheel dispayed inside page
    */
    const timeline = await store.dispatch('timeline/load', { date, cachedOnly: true })

    return {
      showWelcome: false,
      date: timeline ? timeline.date : null,
      timeline
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
      expandedIssues: state => state.timeline.expandedIssues
    }),

    ...mapGetters({
      denormalize: 'entities/denormalize',
    }),

    loading () {
      return !this.showWelcome && this.timeline === null
    },

    timeSlots () {
      if (this.loading) { return [] }

      const { issues } = this.timeline
      const timeSlots = []
      let slot = null

      issues.forEach(issue => {
        if (slot === null || slot.time !== issue.time) {
          slot = { time: issue.time, issues: [] }
          timeSlots.push(slot)
        }

        slot.issues.push(this.denormalize(issue, 'Issue'))
      })

      return timeSlots
    },

    links () {
      if (this.loading) {
        return {}
      }
      return this.timeline.links
    },

    dayTitle () {
      const format = this.$i18n.locale === 'cs' ? 'D.M.' : 'M/D'
      const dt = moment(this.date)
      const today = moment().format(format)
      const day = dt.format(format)
      const wod = day === today ? this.$t('Today') : dt.format('dddd')
      return `${wod} ${day}`
    },
  },

  watch: {
    loggedIn (value) {
      if (value) {
        this.loadTimeline()
        this.$store.dispatch('backlog/loadUserBacklog')
      } else {
        this.date = null
        this.timeline = null
        this.showWelcome = false
      }
    },

    date (value, oldValue) {
      if (process.client && oldValue === null && value !== null && history.state.scrollY) {
        // timeline was loased asynchronously and scroll position was recorded
        Vue.nextTick(() => {
          window.scrollTo(0, history.state.scrollY)
        })
      }
    }
  },

  mounted () {
    if (this.date === null) {
      this.loadTimeline()
    }
    if (this.loggedIn) {
      this.$store.dispatch('backlog/loadUserBacklog')
    }
  },

  methods: {
    async loadTimeline () {
      if (this.loggedIn && !this.$store.state.timeline.hasNoActiveSubscriptions) {
        // TODO load timeline and backlog in parallel
        const { date } = this.$route.params
        const timeline = await this.$store.dispatch('timeline/load', { date })
        if (timeline === null) {
          this.showWelcome = true
        } else {
          this.date = timeline.date
          this.timeline = timeline
        }
      }
    }
  },

  beforeRouteLeave (to, from, next) {
    try {
      if (this.loggedIn) {
        const { history, location } = window
        history.replaceState({ ...history.state, scrollY: window.scrollY }, document.title, location.pathname)
      }
    } finally {
      next()
    }
  },

  head () {
    return {
      title: 'Kairly',
      meta: [
        { hid: 'description', name: 'description', content: 'Timeline showing you latest issues of newspapers you subscribed to.' },
      ]
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- TIMELINE VIEW -//
.timeline-view
  display: block
  padding: $baseline $baseline 0 $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline/2 0 0 0

//- Empty timeline
.timeline--empty
  display: table
  margin: $baseline*2 auto
  padding: $baseline $baseline*2

  background: #fff
  border: 1px solid #ddd

  text-align: center

  @media (max-width: $mobile)
    display: block
    margin: $baseline*2 $baseline
    padding: $baseline

  h2
    margin-bottom: $baseline

    font-weight: 600
    font-size: $fs-1

  p
    margin-bottom: $baseline

  //- links
  > a
    +button
    margin: 0 $baseline/4

//- Header
.timeline--header
  display: flex
  justify-content: space-between

  @media (max-width: $mobile)
    padding: 0 $baseline/4

//- Footer
.timeline--footer
  display: flex
  padding: $baseline 0

  border-top: 3px solid #ddd

  text-align: center

  @media (max-width: $mobile)
    padding: $baseline $baseline/4

  //- you read the entire day title
  p
    flex: 1
    order: 2

    font-family: $ff-serif
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 1.5

//- buttons for switching days
.timeline--footer,
.timeline--header
  a
    position: relative
    z-index: 3

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
      pointer-events: none

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
