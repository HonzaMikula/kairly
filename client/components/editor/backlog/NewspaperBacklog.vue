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

    <SelectionToolbar/>
  </div>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
import { mapActions, mapGetters } from 'vuex'
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

  data() {
    return {
      externalLink: null,
    }
  },

  props: {
    newspaper: Object
  },

  computed: {
    ...mapGetters({
      denormalize: 'entities/denormalize',
    }),

    backlogs() {
      return this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName]
    },

    posts() {
      return mapValues(this.backlogs.$posts, p => this.denormalize(p, 'Post'))
    },

    upcoming() {
      return this.backlogs.upcoming
    },

    next() {
      return this.backlogs.next
    },

    considered() {
      return this.backlogs.considered
    }
  },

  methods: {
    timeFrom(dt) {
      return moment(dt).from()
    }
  }
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
