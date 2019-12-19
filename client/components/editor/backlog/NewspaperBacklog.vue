<template>
  <div class="newspaper-backlog-view">

    <NewspaperBacklogPosts
      :title="$t('Issue #') + (newspaper.issues + 1)"
      :description="$t('Issue will be published ') + timeFrom(newspaper.nextRelease)"
      :newspaper="newspaper"
      :backlog="backlog.upcoming"
      source="upcoming"
    />

    <NewspaperBacklogPosts
      :title="$t('Issue #') + (newspaper.issues + 2)"
      :newspaper="newspaper"
      :backlog="backlog.next"
      source="next"
    />

    <NewspaperBacklogPosts
      :title="$t('Considered posts')"
      :newspaper="newspaper"
      :backlog="backlog.considered"
      source="considered"
    />

    <div class="newspaper-backlog--backlog">
      <div class="newspaper-backlog--backlog--external-article">
        <input
          type="url"
          v-model="externalLink"
          :placeholder="$t('Paste URL of external article')"
        />
        <button
          @click.prevent="addExternalLink">
          {{ $t('Add article') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
import { mapActions } from 'vuex'

import ErrorHandler from '@/mixins/ErrorHandler'
import PostWrapper from '@/components/PostWrapper'
import NewspaperBacklogPosts from '@/components/editor/backlog/NewspaperBacklogPosts'

export default {
  name: 'NewspaperBacklog',

  components: {
    NewspaperBacklogPosts
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
    backlog() {
      const backlog = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName]
      return this.$store.getters['entities/denormalize'](backlog, 'NewspaperBacklog')
    },

    currentMonth() {
      return this.backlog ? this.backlog.currentMonthStats : []
    }
  },

  methods: {
    timeFrom(dt) {
      return moment(dt).from()
    },

    async addExternalLink() {
      const url = this.externalLink
      if (!url) {
        return
      }

      this.$ga.event({
        eventCategory: 'Add external article',
        eventAction: url,
        eventLabel: this.newspaper
      })

      try {
        await this.addLinkToBacklog({newspaper: this.newspaper, url})
        this.externalLink = ''
      } catch (err) {
        this.handleError(err)
      }
    },

    ...mapActions({
      addLinkToBacklog: 'backlog/addLink'
    })
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

//- Backlog
.newspaper-backlog--backlog
  .no-post
    display: flex
    align-items: center
    justify-content: center
    flex-direction: column
    height: 100%
    max-height: 50vh

    color: #999

    &::before
      +fa-icon()
      @extend .fas

      display: block
      margin-bottom: $baseline

      font-size: $fs-4

      content: fa-content($fa-var-newspaper)

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center


//- Add external article
.newspaper-backlog--backlog--external-article
  display: flex
  margin-bottom: $baseline

  input[type=url]
    border: 1px solid #ddd
    border-right: 0
    border-radius: 3px 0 0 3px
    box-sizing: border-box
    flex: 1
    height: $baseline * 1.25
    padding: 0 $baseline/4

    font-family: $ff-sans
    font-size: $fs--1

  button
    border-radius: 0 3px 3px 0
    box-sizing: border-box
    height: $baseline * 1.25

    background: $c-base
    border: 0
    color: #fff

    font-family: $ff-sans
    font-size: $fs--1

    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)

</style>
