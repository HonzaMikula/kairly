<template>
  <div class="newspaper-backlog-view">
    <div
      class="newspaper-backlog--left-column"
      :class="{'is-active': upcomingIssueActive}"
      @click="upcomingIssueActive = true"
    >
      <NewspaperBacklogPosts
        v-if="upcoming"
        :title="$t('Issue #') + (newspaper.issues + 1)"
        :description="$t('Issue will be automatically published ') + timeFrom(newspaper.nextRelease)"
        :newspaper="newspaper"
        :backlog="upcoming"
        :posts="posts"
        source="upcoming"
      />

      <NewspaperBacklogPosts
        :title="$t('Issue #') + (newspaper.issues + 2)"
        :newspaper="newspaper"
        :backlog="next"
        :posts="posts"
        source="next"
      />
    </div>

    <div
      class="newspaper-backlog--right-column"
      :class="{'is-active': !upcomingIssueActive}"
      @click="upcomingIssueActive = false"
    >
      <NewspaperBacklogPosts
        v-if="considered"
        :title="$t('Considered posts')"
        :newspaper="newspaper"
        :backlog="considered"
        :posts="posts"
        source="considered"
      />
    </div>

    <SelectionToolbar
      v-show="selection.length"
      :newspaper="newspaper"
    />
  </div>
</template>

<script>
import moment from 'moment'
import { mapGetters } from 'vuex'
import mapValues from 'lodash/mapValues'

import ErrorHandler from '@/mixins/ErrorHandler'
import NewspaperBacklogPosts from '@/components/editor/backlog/NewspaperBacklogPosts'
import SelectionToolbar from '@/components/editor/backlog/SelectionToolbar'

export default {
  name: 'NewspaperBacklog',

  components: {
    NewspaperBacklogPosts,
    SelectionToolbar
  },

  mixins: [ErrorHandler],

  props: {
    newspaper: { type: Object, required: true }
  },

  data () {
    return {
      externalLink: null,
      upcomingIssueActive: true
    }
  },

  computed: {
    ...mapGetters({
      denormalize: 'entities/denormalize',
      selection: 'backlog/getSelection'
    }),

    backlogs () {
      return this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName]
    },

    posts () {
      return mapValues(this.backlogs.$posts, p => this.denormalize(p, 'Post'))
    },

    upcoming () {
      return this.backlogs.upcoming
    },

    next () {
      return this.backlogs.next
    },

    considered () {
      return this.backlogs.considered
    }
  },

  mounted () {
    window.addEventListener('keydown', this.onKeyDown)
  },

  beforeDestroy () {
    window.removeEventListener('keydown', this.onKeyDown)
  },

  methods: {
    togglePanels () {

    },

    timeFrom (dt) {
      return moment(dt).from()
    },

    onKeyDown (ev) {
      const { newspaper } = this
      let handler = null
      if (this.selection.length) {
        handler = {
          27: () => { // ESC
            this.$store.commit('backlog/cleanSelection')
          },
          38: () => { // arrow UP
            this.$store.dispatch('backlog/moveSelectionUp', { newspaper, target: null })
          },
          40: () => { // arrow DOWN
            this.$store.dispatch('backlog/moveSelectionDown', { newspaper, target: null })
          },
          46: () => { // DEL
            this.$store.dispatch('backlog/removeSelectedBox', { newspaper })
          },
          84: () => { // T
            this.$store.dispatch('backlog/moveSelectionToUpcomingTop', { newspaper })
          },
          71: () => { // B
            this.$store.dispatch('backlog/moveSelectionToUpcomingBottom', { newspaper })
          },
          88: () => { // X
            this.$store.dispatch('backlog/moveSelectionDown', { newspaper, target: 'considered' })
          }
        }[ev.which]
      } else if (ev.which === 27) {
        handler = () => { this.$store.commit('backlog/restoreSelection') }
      }

      if (handler) {
        handler()
        ev.preventDefault()
        ev.stopPropagation()
      }
    },
  },
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'
@import './styles/mixins/scrollbars'

.newspaper-backlog-view
  display: grid
  grid-template-columns: auto auto auto
  max-height: calc(100vh - 300px)

.newspaper-backlog--left-column
    grid-column: 1 / span 2
    grid-row: 1 / span 1

    padding-right: $baseline * 1.5
    height: calc(100vh - 170px)
    overflow-y: auto
    width: 900px

    background: url('~assets/noise-background.png')
    box-shadow: 10px 0 5px -5px #ccc

    +scrollbar

    @media (min-width: 1800px)
      box-shadow: none

    &.is-active
      z-index: 10

.newspaper-backlog--right-column
    grid-column: 2 / span 2
    grid-row: 1 / span 1
    justify-self: end

    height: calc(100vh - 170px)
    overflow-y: auto
    width: 900px
    padding-right: $baseline * 1.5

    background: url('~assets/noise-background.png')
    box-shadow: -10px 0 5px -5px #ccc

    +scrollbar

    @media (min-width: 1800px)
      box-shadow: none

    &.is-active
      z-index: 10

p.newspaper-backlog--info--profit
  strong
    margin-right: $baseline / 2

    color: $c-base

    cursor: pointer

    &:hover,
    &:focus
      darken($c-base, 10%)

.newspaper-backlog-view .post > header
  cursor: move

//- Add external article
.newspaper-backlog--backlog--external-article

</style>
