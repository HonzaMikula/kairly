<template>
  <AppLayout :name="$t('Draft posts')">
    <div class="draft-posts-view">
      <div class="draft-posts--empty" v-if="posts.length == 0">
        <h2>{{ $t('You haven\'t prepared any draft yet.') }}</h2>

        <div class="draft-posts--empty--buttons">
          <nuxt-link to="/posts/create/article">{{ $t('Write an article') }}</nuxt-link>
          <nuxt-link to="/posts/create/tweet">{{ $t('Write a tweet') }}</nuxt-link>
        </div>
      </div>

      <div v-for="post in posts" :key="post.id">
        <PostWrapper
          :post="post"
        >
          <template #page-controls v-if="post.draft">
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

      <PublishPostModal
        :active.sync="isPublishPostDialogOpen"
        :post="modalPost"
        :price="modalPrice"
        @publish="publishPost"
      />
    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import ErrorHandler from '@/mixins/ErrorHandler'
import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'
import PublishPostModal from '@/components/modals/PublishPostModal'

export default {
  name: 'Drafts',

  components: {
    AppLayout,
    PostWrapper,
    PublishPostModal
  },

  mixins: [ErrorHandler],

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
      try {
        await this.$axios.$post(`/drafts/${post.id}/publish`, { price })
        const idx = this.posts.findIndex(p => p.id === post.id)
        this.posts.splice(idx, 1)
      } catch (err) {
        this.handleError(err)
      }
    }
  },

  async asyncData({ store }) {
    return {
      posts: await store.dispatch('getDrafts')
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.draft-posts-view
  max-width: 900px
  margin: $baseline auto

//- Empty placeholder
.draft-posts--empty
  display: block
  margin: $baseline 0

  text-align: center

  h2 
    margin-bottom: $baseline / 2

    font-size: $fs-2
    font-weight: 600

  p
    margin-bottom: $baseline

.draft-posts--empty--buttons
  display: flex
  justify-content: center

  a
    +button
    margin: 0 $baseline/4

</style>
