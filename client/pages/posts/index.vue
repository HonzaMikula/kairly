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
            <template v-if="post.draft" #page-controls>
              <button @click="openPublishDialog(post)">{{ $t('Publish') }}</button>

              <button-icon
                v-b-tooltip
                class="edit"
                :title="$t('Edit post')"
                tabindex="0"
                role="button"
                @click.prevent="$router.push(`/posts/${post.id}`)"
              />

              <button-icon
                v-b-tooltip
                class="remove"
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

  components: {
    AppLayout,
    PostWrapper,
    PublishPostModal,
    EmptyPostPlaceholder
  },

  mixins: [ErrorHandler],

  async asyncData ({ store }) {
    return {
      posts: await store.dispatch('getDrafts')
    }
  },

  data () {
    return {
      isPublishPostDialogOpen: null,
      modalPost: null,
      modalPrice: null
    }
  },

  head () {
    return {
      title: this.$t('Draft Posts – Kairly')
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  methods: {
    async deletePost (post) {
      if (confirm('Are you sure?')) {
        await this.$axios.$delete(`/drafts/${post.id}`)
        const idx = this.posts.findIndex(p => p.id === post.id)
        if (idx !== -1) {
          this.posts.splice(idx, 1)
        }
      }
    },

    async openPublishDialog (post) {
      const { price: fairPrice } = await this.$axios.$get(`/drafts/${post.id}/fair-price`)

      this.modalPrice = fairPrice
      this.modalPost = post
      this.isPublishPostDialogOpen = true
    },

    async publishPost (price) {
      const post = this.modalPost
      try {
        await this.$axios.$post(`/drafts/${post.id}/publish`, { price })
        const idx = this.posts.findIndex(p => p.id === post.id)
        this.posts.splice(idx, 1)
      } catch (err) {
        this.handleError(err)
      }
    }
  }
}
</script>

<style lang="sass">
.draft-posts-view
  max-width: 900px
  margin: $baseline auto
</style>
