<template>
  <app-layout>
    <timeline-view>
      <Welcome v-if="noSsubscriptions"/>
      <div v-else>
        <div class="timeline-navigation">
          <button
            @click="showJumpMenu = !showJumpMenu"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            title="Jump to different time"
          >Today 9/25 – 06:00</button>

          <a v-if="nextDay" href="#" @click.prevent="loadTimeline(nextDay)">Show {{ nextDay }}</a>
          <a href="#" @click.prevent="loadTimeline(prevDay)">Show {{ prevDay }}</a>

          <div
            v-if="showJumpMenu"
            v-on-clickaway="() => showJumpMenu = false"
            class="timeline-navigation--menu">
            <header>
              <button-icon tabindex="0"></button-icon>
              <h3>Today 9/25</h3>
              <button-icon tabindex="0"></button-icon>
            </header>

            <section>
              <ul>
                <li><a href="">Early morning (6:00)</a></li>
                <li><a href="">Morning (9:00)</a></li>
                <li><a href="">Noon (12:00)</a></li>
                <li><a href="">Afternoon (15:00)</a></li>
                <li><a href="">Evening (18:00)</a></li>
                <li><a href="">Night (21:00)</a></li>
              </ul>
            </section>
          </div>
        </div>

        <div v-if="issues.length">
          <IssueWrapper v-for="issue in issues"
            :key="issue.id"
            :issue="issue"
            :subscription="true"
            :expanded="expandedIssues[issue.id]" />
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
import { directive as onClickaway } from '@/lib/vue-clickaway'
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

  directives: {
    onClickaway
  },

  data() {
    return {
      showJumpMenu: false,
      noSsubscriptions: false,
      loading: true,
      issues: [],
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
        this.noSsubscriptions = true
        this.loading = false
        return
      }

      date = response.data.date
      const { issues, links } = response.data

      this.issues = issues
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


.timeline-navigation
  position: relative

  margin-bottom: $baseline

  text-align: center

  &::before,
  &::after
    position: absolute

    border-radius: 100%
    height: 7px
    width: 7px

    background: #ddd

    content: ''

  &::before
    margin: 11px 0 0 -30px

  &::after
    margin: 11px 0 0 25px


  button
    display: inline-block
    border-radius: $baseline/2
    height: $baseline
    padding: 0 $baseline/2
    margin-bottom: $baseline /4

    background: #eee
    border: 0

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0


    &:focus,
    &:hover
      background: #ddd

.timeline-navigation--menu
  +context-menu

  li a span
    border-radius: 100%
    display: inline-block
    float: right
    padding: 0 $baseline/4
    margin-top: 6px

    background: #ddd

    line-height: $baseline * 0.8


</style>
