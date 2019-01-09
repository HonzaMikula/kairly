<template>
  <my-posts>
    <div class="my-posts--empty" v-if="posts.length == 0">
      {{ $t('No drafts') }}
    </div>

    <div v-for="post in posts" :key="post.id">
      <PostWrapper
        :post="post"
        :isSubscribed="true"
      >
        <template slot="controls" v-if="post.draft">
          <button @click="publishPost(post)">{{ $t('Publish') }}</button>

          <button-icon
            class="edit"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="$t('Edit post')"
            tabindex="0"
            role="button"
            @click.prevent="$router.push(`/posts/${post.id}`)">
          </button-icon>

          <button-icon
            class="remove"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="$t('Delete post')"
            tabindex="0"
            role="button"
            @click.prevent="deletePost(post)">
          </button-icon>

        </template>
      </PostWrapper>
    </div>
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

  async asyncData({ app, store, params }) {
    const { posts } = await app.$axios.$get(`/drafts`)
    return {
      posts
    }
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
