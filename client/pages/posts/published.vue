<template>
  <my-posts>
    <PostWrapper
      v-for="post in posts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    >
      <template slot="controls">
        <button-icon
          class="edit"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
          title="Edit post"
          @click.prevent="$router.push(`/posts/${post.id}`)">
        </button-icon>
      </template>
    </PostWrapper>

    <div v-if="!posts.length && !loadingPosts" class="my-posts--empty">
      <p>{{ $t("You didn't publish any post.") }}</p>
    </div>

    <loading-spinner v-if="loadingPosts"></loading-spinner>
  </my-posts>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import MyPosts from '@/components/layout/MyPosts'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'Drafts',

  components: {
    MyPosts,
    PostWrapper
  },

  data() {
    return {
      posts: [],
      cursor: 0,
      loadingPosts: true
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  methods: {
    async loadPosts() {
      if (this.cursor === null) {
        return
      }
      const { author: authorId } = this.$route.params

      this.loadingPosts = true

      const { posts, cursor } = await this.$axios.$get(
        `/authors/${this.user.id}/posts`, {params: {cursor: this.cursor}})

      posts.forEach(post => this.posts.push(post))
      this.cursor = cursor
      this.loadingPosts = false
    }
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },

  created() {
    this.loadPosts()
  }
}
</script>

<style lang="sass">
//- Empty placeholder
.my-posts--empty
  display: block
  margin: $baseline 0
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center
</style>
