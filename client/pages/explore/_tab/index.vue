<template>
  <main>
    <loading-spinner v-if="loading"></loading-spinner>

    <div
      v-else-if="timeline"
      class="timeline-view explore-timeline-view"
    >
      <header class="explore--controls">
        <nuxt-link :to="`/explore/${tab.slug}/newspapers-authors`">
          {{ $t('See all authors') }}
        </nuxt-link>

        <div>
          <label for="onlyNewspapers">{{ $t('Only newspapers') }}</label>
          <label class="switch">
            <input 
              type="checkbox" 
              v-model="mode"
              true-value="all"
              false-value="newspapers"
              id="onlyNewspapers"
            />
            <span class="slider round"></span>
          </label>
        </div>
      </header>
      
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
