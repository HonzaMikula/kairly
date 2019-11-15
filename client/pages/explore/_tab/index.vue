<template>
  <main>
    <loading-spinner v-if="loading"></loading-spinner>

    <div
      v-else-if="timeline"
      class="timeline-view"
    >
      <nuxt-link :to="`/explore/${tab.slug}/newspapers-authors`">Explore list of newspapers & authors</nuxt-link>
      <br>
      Show: <a href="" @click.prevent="mode = 'all'">Nespapers & Authors</a> | <a href=""  @click.prevent="mode = 'newspapers'">Nespapers only</a>


      <header
          v-if="!loading"
          class="timeline--header"
        >
          <nuxt-link
            :to="`/explore/${tab.slug}/${links.prev}`"
            v-b-tooltip
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          />

          <nuxt-link
            v-if="links.next"
            :to="`/explore/${tab.slug}/${links.next}`"
            v-b-tooltip
            :title="'Next day ('+ links.next +')'"
            :class="['next', {'is-disabled': !links.next}]"
          />
        </header>

      <template v-for="timeSlot in timeSlots">
        <JumpMenu
          :key="timeSlot.time"
          :datetime="timeSlot.time"
          :timeSlots="timeSlots"
        />

        <IssueWrapper
          v-for="issue in timeSlot.issues"
          :key="issue.id"
          :issue="issue"
          :subscription="true"
        />
      </template>
    </div>
  </main>
</template>

<script>
import TABS from '@/exploreTabs'

import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'

export default {
  name: 'ExploreTab',

  //auth: false,

  components: {
    IssueWrapper,
    JumpMenu
  },

  head() {
    const title = this.tab[this.$i18n.locale || 'en']
    return {
      title:  `${title} – Explore – Kairly`
    }
  },

  data() {
    return {
      loading: true,
      timeline: null,
      mode: 'all',
    }
  },

  computed: {
    tab() {
      return TABS.find(t => t.slug === this.$route.params.tab)
    },

    links() {
      if (this.loading) {
        return {}
      }
      return this.timeline.links
    },

    timeSlots() {
      if (this.loading) { return [] }

      const { mode } = this
      const { issues } = this.timeline
      const timeSlots = []
      let slot = null

      issues.forEach(issue => {
        if (mode === 'newspapers' && issue.type === 'author') {
          return
        }
        if (slot === null || slot.time !== issue.time) {
          slot = { time: issue.time, issues: []}
          timeSlots.push(slot)
        }
        slot.issues.push(issue)
      })

      return timeSlots
    },
  },

  watch:{
    $route (to, from){
      this.loadTimeline()
    }
  },

  methods: {
    async loadTimeline() {
      this.loading = true

      // TODO support historical timelines
      const { date } = this.$route.params
      const endpoint = `/explore-timeline/${this.tab.slug}`
      const timeline  = await this.$store.dispatch('timeline/load', { endpoint, date })
      this.timeline = timeline
      this.loading = false
    }
  },

  mounted() {
    this.loadTimeline()
  }
}
</script>

<style lang="sass">
// copies from index
.timeline-view
  display: block
  padding: $baseline $baseline 0 $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline/2 0 0 0

explore-view
  section button
    display: table
    border-radius: $baseline
    height: $baseline * 1.25
    padding: 0 $baseline
    margin: 0 auto

    background: $c-base
    border: 0
    color: #fff

    font-family: $ff-sans
    font-size: $fs-0
    line-height: $baseline * 1.25
    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)


</style>
