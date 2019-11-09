<template>
  <main>
    <loading-spinner v-if="loading"></loading-spinner>

    <div
      v-else
      class="timeline-view"
    >
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

//import NewspaperWidget from '@/components/widgets/NewspaperWidget'
//import AuthorWidget from '@/components/widgets/AuthorWidget'

import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'
//import ExploreModal from '@/components/modals/ExploreModal'

export default {
  name: 'ExploreTab',

  //auth: false,

  components: {
    IssueWrapper,
    JumpMenu
    //NewspaperWidget,
    //AuthorWidget,
    //ExploreModal
  },

  head() {
    return {
      title: this.tab ? `${this.tab.name} – Explore – Kairly` : 'Explore – Kairly',
    }
  },

  data() {
    const tab = TABS.find(t => t.slug === this.$route.params.tab)

    return {
      loading: true,
      timeline: null,
      tab,
    }
  },

  computed: {
    timeSlots() {
      if (this.loading) { return [] }

      const { issues } = this.timeline
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
  },

  methods: {
    async loadTimeline() {
      const timeline  = await this.$store.dispatch('timeline/load', { date: null })
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
