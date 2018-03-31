<template>
  <component
    :is="'issue-' + issue.type"
    :issue="issue"
    :key="issue.id">

    <PostWrapper
      v-for="post in headPosts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    />

    <a href="#" v-if="hasMore"
      v-on:click.prevent="togglePosts">
        ---------------
        {{ showAllPosts ? "Hide more posts" : "Show more posts" }}
        ---------------
    </a>

    <PostWrapper
      v-for="post in tailPosts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    />

  </component>
</template>

<script>
import issueEdition from '@/components/issues/edition'
import issueAuthor from '@/components/issues/author'
import PostWrapper from '@/components/PostWrapper'

const POST_LIMIT = 5

export default {
  name: 'IssueWrapper',
  props: ['issue'],

  components: {
    issueEdition,
    issueAuthor,
    PostWrapper,
  },

  data: function() {
    return {
      showAllPosts: false
    }
  },

  computed: {
    headPosts() {
      return this.issue.posts.slice(0, POST_LIMIT)
    },

    tailPosts() {
      return this.showAllPosts ? this.issue.posts.slice(POST_LIMIT) : []
    },

    hasMore() {
      return this.issue.posts.length > POST_LIMIT
    }
  },

  methods: {
    togglePosts() {
      this.showAllPosts = !this.showAllPosts
    }
  }
}
</script>
