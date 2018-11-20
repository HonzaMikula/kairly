<template>
  <component
    :is="'issue-' + issue.type"
    :issue="issue"
    :key="issue.id"
    :hideDate="hideDate">

    <template slot="newspaperTitle"><slot name="newspaperTitle"></slot></template>

    <PostWrapper
      v-for="post in headPosts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    />

    <PostWrapper
      v-for="post in tailPosts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    />

    <footer>
      <button v-if="tailPostsCount > 0 && !expanded" @click.prevent="expandIssue">
        Show more ({{tailPostsCount}})
      </button>
    </footer>

  </component>
</template>

<script>
import issueNewspaper from '@/components/issues/newspaper'
import issueAuthor from '@/components/issues/author'
import PostWrapper from '@/components/PostWrapper'

const POST_LIMIT = 5

export default {
  name: 'IssueWrapper',
  props: {
    issue: Object,
    subscription: Boolean,
    hideDate: Boolean,
  },

  components: {
    issueNewspaper,
    issueAuthor,
    PostWrapper,
  },

  data() {
    return {
      showAllPosts: false
    }
  },

  computed: {
    expanded() {
      return !!this.$store.state.timelineExpandedIssues[this.issue.id]
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

      font-size: $fs-3
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

  footer
    text-align: center

    button
      display: table
      border-radius: $baseline
      height: $baseline * 1.25
      padding: 0 $baseline
      margin: 0 auto

      background: $c-base
      border: 0
      color: #fff

      font-family: $ff-sans
      font-size: $fs--1
      line-height: $baseline * 1.25
      cursor: pointer

      &:hover,
      &:focus
        background: darken($c-base, 10%)
</style>
