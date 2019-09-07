<template>
  <div class="newspaper-backlog-view">

    <!-- <NewspaperBacklogInfo
      :newspaper="newspaper"
      :current-month="currentMonth"
      :published="upcomingIssue.map(log => log.post)"
    /> -->

    <NewspaperBacklogPosts
      :title="'Issue #' + (newspaper.issues + 1)"
      :description="'Issue will be published '+ timeFrom(newspaper.nextRelease)"
      :newspaper="newspaper"
      :backlog="backlog.upcoming"
      source="upcoming"
    />

    <NewspaperBacklogPosts
      :title="'Issue #'+ (newspaper.issues + 2)"
      :newspaper="newspaper"
      :backlog="backlog.next"
      source="next"
    />

    <NewspaperBacklogPosts
      title="Considered posts"
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
import { mapActions, mapMutations } from 'vuex'

import PostWrapper from '@/components/PostWrapper'
//import NewspaperBacklogInfo from '@/components/editor/backlog/NewspaperBacklogInfo'
import NewspaperBacklogPosts from '@/components/editor/backlog/NewspaperBacklogPosts'
//import BacklogPost from '@/components/editor/backlog/BacklogPost'


export default {
  name: 'NewspaperBacklog',

  components: {
    //BacklogPost,
    //NewspaperBacklogInfo,
    NewspaperBacklogPosts
  },

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
      return this.$store.state.newspaperBacklog[this.newspaper.fullName]
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
        if (err.response.status >= 400) {
          this.showError(err.response.data.error)
        } else {
          this.showError((err + '') || 'Request failed')
        }
      }
    },

    // ...mapActions([
    //     'removeFromNewspaperBacklog', 'addLinkToBacklog',
    //     'backlogMoveDown', 'backlogMoveUp',
    //     'backlogPublish', 'backlogUndoPublish'
    // ]),
    ...mapMutations(['showError'])
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

// .newspaper-backlog-view
//   > div
//     display: grid
//     grid-template-columns: 970px auto
//     grid-column-gap: $baseline

p.newspaper-backlog--info--profit
  strong
    margin-right: $baseline / 2

    color: $c-base

    cursor: pointer

    &:hover,
    &:focus
      darken($c-base, 10%)

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
