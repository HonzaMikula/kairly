<template>
  <app-layout>
    <div style="margin: 40px auto; width: 800px">
      <h1>My posts</h1>

      <br/>

      <div class="create-post-link">
        <nuxt-link to="/posts/create">Create a post</nuxt-link>
      </div>

      <br/>

      <div v-for="post in posts" :key="post.id">
        <PostWrapper
          :post="post"
          :isSubscribed="true"

        >
          <template slot="controls">
            <button-icon v-if="post.draft"
              class="remove"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              title="Delete post"
              @click.prevent="deletePost(post)">
            </button-icon>
          </template>
        </PostWrapper>

        <!-- if used this way move as template slot inside PostWrapper -->
        <div v-if="post.draft" class="post-buttons" style="background-color: white; margin-top: -15px; padding: 20px">
          <nuxt-link :to="`/posts/${post.id}`">Edit</nuxt-link>
          <button @click="publishPost(post)">Publish</button>
        </div>
      </div>


    </div>
  </app-layout>
</template>


<script>


import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'Posts',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
    }
  },

  components: {
    AppLayout,
    PostWrapper
  },


  data() {
    return {

    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  methods: {
    async deletePost(post) {
      if (confirm("Are you sure?")) {
        await this.$axios.$delete(`/drafts/${post.id}`)
        const idx = this.posts.findIndex(p => p.id === post.id)
        if (idx !== -1) {
          this.posts.splice(idx, 1)
        }
      }
    },

    async publishPost(post) {
      const { post: publishedPost } = await this.$axios.$post(`/drafts/${post.id}/publish`)
      const idx = this.posts.findIndex(p => p.id === post.id)
      this.posts.splice(idx, 1, publishedPost)
    }
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },

  async asyncData({ app, store, params }) {
    const { posts } = await app.$axios.$get(`/drafts`)
    return {
      posts
    }
  }
}
</script>

<style lang="sass">
.post-buttons, .create-post-link
  a, button
    +subscribe-button

    height: $baseline * 1.25

    border-radius: $baseline*0.75
    background: $c-base
    color: #fff

    font-family: $ff-sans
    font-size: $fs-0

    &:focus,
    &:hover
      background: darken($c-base, 10%)

.create-post-link a
  font-size: $fs-2
</style>
