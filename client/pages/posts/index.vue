<template>
  <MyPosts>
    <div class="my-posts--empty" v-if="posts.length == 0">
      {{ $t('No drafts') }}
    </div>

    <div v-for="post in posts" :key="post.id">
      <PostWrapper
        :post="post"
        :isSubscribed="true"
      >
        <template #controls v-if="post.draft">
          <button @click="openPublishDialog(post)">{{ $t('Publish') }}</button>

          <button-icon
            class="edit"
            v-b-tooltip
            :title="$t('Edit post')"
            tabindex="0"
            role="button"
            @click.prevent="$router.push(`/posts/${post.id}`)"
          />

          <button-icon
            class="remove"
            v-b-tooltip
            :title="$t('Delete post')"
            tabindex="0"
            role="button"
            @click.prevent="deletePost(post)"
          />

        </template>
      </PostWrapper>
    </div>

    <portal to="modal" v-if="isPublishPostDialogOpen">
      <PublishPostDialog
        :post="modalPost"
        :price="modalPrice"
        @publish="publishPost">
      </PublishPostDialog>
    </portal>
  </MyPosts>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

import MyPosts from '@/components/layout/MyPosts'
import PostWrapper from '@/components/PostWrapper'
import PublishPostDialog from '@/components/modals/PublishPost'

export default {
  name: 'Drafts',

  components: {
    MyPosts,
    PostWrapper,
    PublishPostDialog
  },

  data() {
    return {
      isPublishPostDialogOpen: null,
      modalPost: null,
      modalPrice: null
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  methods: {
    ...mapMutations(['showError']),

    closePublishDialog() {
      this.isPublishPostDialogOpen = false
    },

    async deletePost(post) {
      if (confirm("Are you sure?")) {
        await this.$axios.$delete(`/drafts/${post.id}`)
        const idx = this.posts.findIndex(p => p.id === post.id)
        if (idx !== -1) {
          this.posts.splice(idx, 1)
        }
      }
    },

    async openPublishDialog(post) {
      const { price: fairPrice } = await this.$axios.$get(`/drafts/${post.id}/fair-price`)

      this.modalPrice = fairPrice
      this.modalPost = post
      this.isPublishPostDialogOpen = true
    },

    async publishPost(price) {
      const post = this.modalPost
      this.isPublishPostDialogOpen = false

      try {
        if (price === null) {
          // user cancels
          return
        }

        const { post: publishedPost } = await this.$axios.$post(`/drafts/${post.id}/publish`, { price })
        const idx = this.posts.findIndex(p => p.id === post.id)
        this.posts.splice(idx, 1, publishedPost)
      } catch (err) {
        if (err.response && err.response.status === 400) {
          this.showError(err.response.data.error)
        } else {
          this.showError((err + '') || 'Request failed')
        }
      }
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
