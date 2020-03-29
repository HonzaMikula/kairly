<template>
  <main>
    <div class="explore-timeline-view">
      <header class="explore--controls" v-if="!disableControls">
        <nuxt-link :to="`/explore/${category.slug}/newspapers-authors`">
          {{ $t('See all authors') }}
        </nuxt-link>

        <div>
          <label for="onlyNewspapers">{{ $t('Only newsletters') }}</label>
          <label class="switch">
            <input
              type="checkbox"
              v-model="mode"
              true-value="newspapers"
              false-value="all"
              id="onlyNewspapers"
            />
            <span class="slider round"></span>
          </label>
        </div>
      </header>

      <TimelineLoader v-if="loading" />

      <template v-else>
        <header class="timeline--header">
          <nuxt-link
            :to="`/explore/${category.slug}/${links.prev}`"
            v-b-tooltip
            :title="'Previous day ('+ links.prev +')'"
            class="previous"
          />

          <nuxt-link
            v-if="links.next"
            :to="`/explore/${category.slug}/${links.next}`"
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
      </template>
    </div>
  </main>
</template>

<script>
import { mapGetters } from 'vuex'

import IssueWrapper from '@/components/IssueWrapper'
import JumpMenu from '@/components/widgets/JumpMenu'
import TimelineLoader from '@/components/widgets/TimelineLoader'

export default {
  name: 'ExploreTimeline',

  components: {
    IssueWrapper,
    JumpMenu,
    TimelineLoader
  },

  props: {
    disableControls: Boolean,
    category: Object,
    period: String
  },

  data() {
    return {
      loading: true,
      timeline: null,
      mode: 'all',
    }
  },

  computed: {
    ...mapGetters({
      denormalize: 'entities/denormalize',
    }),

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

        slot.issues.push(this.denormalize(issue, 'Issue'))
      })

      return timeSlots
    },
  },

  watch:{
    category: function() {
      this.loadTimeline()
    },

    period: function() {
      this.loadTimeline()
    }
  },

  methods: {
    async loadTimeline() {
      this.loading = true

      // TODO support historical timelines
      const { date } = this.$route.params
      const endpoint = `/explore-timeline/${this.category.slug}`
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
@import './styles/components/buttons'

// copies from index
.explore-timeline-view
  display: block
  padding: $baseline $baseline 0 $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline/2 0 0 0


//- Controls
.explore--controls
  display: flex
  align-items: center
  justify-content: space-between
  padding-bottom: $baseline

  @media (max-width: $mobile)
    padding: 0 $baseline/4 $baseline $baseline/4

  a
    +button-icon($fa-var-clipboard-list, icon-text)

    background: #fff
    color: #555

    @media (max-width: $mobile)
      padding-right: $baseline / 2

    &:focus,
    &:hover
      background: #ddd
      color: #000


  //- Toggle
  .switch
    position: relative
    display: inline-block
    width: $baseline * 2
    height: $baseline

    input
      opacity: 0
      width: 0
      height: 0

    .slider
      position: absolute
      cursor: pointer
      top: 0
      left: 0
      right: 0
      bottom: 0
      background-color: #ccc
      transition: .4s

    .slider:before
      position: absolute
      content: ""
      height: ($baseline - 4px)
      width: ($baseline - 4px)
      left: 2px
      bottom: 2px
      background-color: white
      transition: .4s

    input:checked + .slider
      background-color: $c-base

    input:focus + .slider
      box-shadow: 0 0 1px $c-base

    input:checked + .slider:before
      transform: translateX(($baseline))

    /* Rounded sliders */
    .slider.round
      border-radius: $baseline

    .slider.round:before
      border-radius: 50%

</style>
