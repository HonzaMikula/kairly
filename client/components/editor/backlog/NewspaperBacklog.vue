<template>
  <div class="newspaper-backlog-view">
    <NewspaperBacklogPosts
      v-if="upcoming"
      :title="$t('Issue #') + (newspaper.issues + 1)"
      :description="$t('Issue will be published ') + timeFrom(newspaper.nextRelease)"
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

    <NewspaperBacklogPosts
      v-if="considered"
      :title="$t('Considered posts')"
      :newspaper="newspaper"
      :backlog="considered"
      :posts="posts"
      source="considered"
    />

    <SelectionToolbar
      v-show="selectionSize > 0"
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
    newspaper: Object
  },

  data () {
    return {
      externalLink: null,
    }
  },

  computed: {
    ...mapGetters({
      denormalize: 'entities/denormalize',
    }),

    selectionSize () {
      return Object.keys(this.$store.state.backlog.selection).length
    },

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
    window.addEventListener('keyup', this.onKeyUp)
  },

  beforeDestroy () {
    window.removeEventListener('keyup', this.onKeyUp)
  },

  methods: {
    timeFrom (dt) {
      return moment(dt).from()
    },

    onKeyUp (event) {
      if (this.$store.getters['backlog/getSelection'].length) {
        if (event.which === 27) { // esc
          this.$store.commit('backlog/cleanSelection')
        } else if (event.which === 38) { // arrow up
          this.$store.dispatch('backlog/moveSelectionUp', {
            newspaper: this.newspaper,
            target: null
          })
        } else if (event.which === 40) { // arrow down
          this.$store.dispatch('backlog/moveSelectionDown', {
            newspaper: this.newspaper,
            target: null
          })
        } else if (event.which === 46) { // del
          this.$store.dispatch('backlog/removeSelectedBox', {
            newspaper: this.newspaper
          })
        } else if (event.which === 84) { // t
          this.$store.dispatch('backlog/moveSelectionToUpcomingTop', {
            newspaper: this.newspaper
          })
        } else if (event.which === 66) { // b
          this.$store.dispatch('backlog/moveSelectionDown', {
            newspaper: this.newspaper,
            target: 'considered'
          })
        }
      }
    },
  },
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

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
