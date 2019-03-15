<template>
  <component
    :is="componentName"
    :key="issue.id"
    :issue="issue"
    :hideDate="hideDate">

    <template slot="newspaperTitle">
      <slot name="newspaperTitle"/>
    </template>

    <PostWrapper
      v-for="post in headPosts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    />

    <PostWrapper
      v-for="post in tailPosts"
      :key="post.id"
      :post="post"
      :isSubscribed="true"
    />

    <footer class="issue--footer">
      <div class="issue--footer--show-more">
        <button
          v-if="(tailPostsCount > 0 && !expanded)"
          @click.prevent="expandIssue">
          {{ $t('Show more') }} ({{tailPostsCount}})
        </button>
      </div>

      <div class="issue--footer--recommend-button">
        <RecommendButtonIssue
          v-if="loggedIn && issue.type == 'newspaper'"
          :issue="issue"
        />
      </div>
    </footer>
  </component>
</template>

<script>
import { mapState } from 'vuex'

import IssueSuspendedAuthor from '@/components/issues/IssueSuspendedAuthor'
import IssueSuspendedNewspaper from '@/components/issues/IssueSuspendedNewspaper'
import IssueUnreleasedNewspaper from '@/components/issues/IssueUnreleasedNewspaper'
import IssueNewspaper from '@/components/issues/IssueNewspaper'
import IssueAuthor from '@/components/issues/IssueAuthor'
import PostWrapper from '@/components/PostWrapper'
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'

const POST_LIMIT = 5

export default {
  name: 'IssueWrapper',

  props: {
    issue: Object,
    subscription: Boolean,
    hideDate: Boolean,
    showTail: Boolean
  },

  components: {
    IssueAuthor,
    IssueNewspaper,
    IssueSuspendedAuthor,
    IssueSuspendedNewspaper,
    IssueUnreleasedNewspaper,
    PostWrapper,
    RecommendButtonIssue
  },

  data() {
    return {
      showAllPosts: false
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
        return !!this.$store.state.timelineExpandedIssues[this.issue.id]
      }
    },

    headPosts() {
      return this.issue.posts.slice(0, POST_LIMIT)
    },

    tailPosts() {
      return this.expanded ? this.issue.posts.slice(POST_LIMIT) : []
    },

    tailPostsCount() {
      return Math.max(0, this.issue.posts.length - POST_LIMIT)
    }

  },

  methods: {
    expandIssue() {
      this.$store.dispatch('expandIssue', this.issue.id)
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Newspaper
timeline-newspaper
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

  > div
    margin: 0 $baseline/4

//- show more button
.issue--footer--show-more button
  +button

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
