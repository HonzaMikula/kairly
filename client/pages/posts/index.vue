<template>
  <AppLayout :name="$t('Draft posts')">
    <div class="draft-posts-view">
      <EmptyPostPlaceholder v-if="posts.length == 0">
        {{ $t('You haven\'t prepared any draft yet.') }}
      </EmptyPostPlaceholder>

      <template v-else>
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
      </template>
    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import ErrorHandler from '@/mixins/ErrorHandler'
import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'
import PublishPostModal from '@/components/modals/PublishPostModal'
import EmptyPostPlaceholder from '@/components/editor/EmptyPostPlaceholder'

export default {
  name: 'Drafts',

  head() {
    return {
      title: this.$t('Draft Posts – Kairly')
    }
  },

  components: {
    AppLayout,
    PostWrapper,
    PublishPostModal,
    EmptyPostPlaceholder
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
.draft-posts-view
  max-width: 900px
  margin: $baseline auto
</style>