<template>
  <component
    :is="componentName"
    :key="issue.id"
    :issue="issue"
    :hideDate="hideDate">

    <template #newspaper-title>
      <slot name="newspaper-title"/>
    </template>

    <component
      v-for="(post, idx) in headPosts"
      :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
      :key="`head-${idx}`"
      :post="post"
    />

    <component
      v-for="(post, idx) in tailPosts"
      :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
      :key="`tail-${idx}`"
      :post="post"
    />

    <footer class="issue--footer">
      <button
        class="show-more"
        v-if="(tailPostsCount > 0 && !expanded)"
        @click.prevent="expandIssue">
        {{ $t('Show more') }} ({{tailPostsCount}})
      </button>

      <RecommendButtonIssue
        v-if="loggedIn && issue.type == 'newspaper'"
        :issue="issue"
      />
      <button
        v-if="issue.type == 'newspaper'"
        class="share"
        :title="$t('Share')"
        :aria-label="$t('Share')"
        @click="openShareModal()"
       >
      </button>
    </footer>

    <ShareModal
      :active.sync="isShareModalOpen"
      :issue="issue"
    />
  </component>
</template>

<script>
import { mapState } from 'vuex'

import PostObjectMixin from '@/mixins/PostObjectMixin'

import IssueSuspendedAuthor from '@/components/issues/IssueSuspendedAuthor'
import IssueSuspendedNewspaper from '@/components/issues/IssueSuspendedNewspaper'
import IssueUnreleasedNewspaper from '@/components/issues/IssueUnreleasedNewspaper'
import IssueNewspaper from '@/components/issues/IssueNewspaper'
import IssueAuthor from '@/components/issues/IssueAuthor'
import PostWrapper from '@/components/PostWrapper'
import BoxWrapper from '@/components/BoxWrapper'
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'
import ShareModal from '@/components/modals/ShareModal'

const POST_LIMIT = 5

export default {
  name: 'IssueWrapper',

  props: {
    issue: Object,
    subscription: Boolean,
    hideDate: Boolean,
    showTail: Boolean
  },

  mixins: [PostObjectMixin],

  components: {
    IssueAuthor,
    IssueNewspaper,
    IssueSuspendedAuthor,
    IssueSuspendedNewspaper,
    IssueUnreleasedNewspaper,
    PostWrapper,
    BoxWrapper,
    RecommendButtonIssue,
    ShareModal
  },

  data() {
    return {
      showAllPosts: false,
      isShareModalOpen: false,
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    componentName() {
      return 'issue-' + this.issue.type
    },

    expanded() {
      if (this.showTail) {
        return true
      }
      else {
        return !!this.$store.state.timeline.expandedIssues[this.issue.id]
      }
    },

    // postsById() {
    //   return keyBy(this.issue.posts, 'id')
    // },

    headPosts() {
      return this.issue.layout.slice(0, POST_LIMIT).map(item => this.getPostObject(item))
    },

    tailPosts() {
      return this.expanded ? this.issue.layout.slice(POST_LIMIT).map(item => this.getPostObject(item)) : []
    },

    tailPostsCount() {
      return Math.max(0, this.issue.layout.length - POST_LIMIT)
    }

  },

  methods: {
    expandIssue() {
      this.$store.dispatch('timeline/expandIssue', this.issue.id)
    },

    openShareModal() {
      this.isShareModalOpen = true
      this.$ga.event({
        eventCategory: 'Share',
        eventAction: 'Open Share modal'
      })
    },
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Newspaper
.timeline-newspaper
  display: block
  margin: $baseline*2 0 $baseline

  > header
    margin-bottom: $baseline

    font-family: $ff-serif
    text-align: center

    h1
      margin-bottom: $baseline / 4

      font-size: $fs-2
      line-height: $baseline * 1.25

      img
        float: left
        height: $baseline * 1.25
        margin-right: $baseline / 4
        width: $baseline * 1.25

      a
        display: inline-block

        color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: bottom

    p
      font-size: $fs-0

      color: #999

      a
        color: #999

      @media (max-width: $mobile)
        span
          display: none

//- Footer
.issue--footer
  display: flex
  justify-content: center

  > *
    margin-right: $baseline / 2

    &:last-of-type
      margin-right: 0

  //- show more button
  .show-more
    +button

  .share
     +button-icon($fa-var-share-alt, icon-text)

//- Issue
.issue-footer
  text-align: center

  button
    display: inline-block
    border-radius: $baseline * 0.7
    height: $baseline * 1.25
    padding: 0 $baseline/2

    background: transparent
    border: 1px solid #ddd
    color: #555

    font-size: $fs-0
    font-family: $ff-sans
    line-height: $baseline * 1.25

    cursor: pointer

    &:hover,
    &:focus
      border: 1px solid $c-base
      color: $c-base
</style>
