<template>
  <AppLayout :name="$t('Published posts')">
    <div class="published-posts-view">
      <PostWrapper
        v-for="post in posts"
        :key="post.id"
        :post="post"
      >
        <template #page-controls>
          <button-icon
            v-b-tooltip
            class="edit"
            :title="$t('Edit post')"
            @click.prevent="$router.push(`/posts/${post.id}`)"
          />
        </template>
      </PostWrapper>

      <EmptyPostPlaceholder v-if="!posts.length && !loadingPosts">
        {{ $t('You haven\'t published any post yet.') }}
      </EmptyPostPlaceholder>

      <loading-spinner v-if="loadingPosts" />
    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'
import EmptyPostPlaceholder from '@/components/editor/EmptyPostPlaceholder'

export default {
  name: 'Published',

  components: {
    AppLayout,
    PostWrapper,
    EmptyPostPlaceholder
  },

  data () {
    return {
      posts: [],
      cursor: 0,
      loadingPosts: true
    }
  },

  head () {
    return {
      title: this.$t('Published Posts – Kairly')
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  created () {
    this.loadPosts()
  },

  methods: {
    async loadPosts () {
      if (this.cursor === null) {
        return
      }

      this.loadingPosts = true

      const params = {
        authorId: this.user.id,
        cursor: this.cursor,
        skipRecommendations: 1
      }
      const { posts, cursor } = await this.$store.dispatch('getAuthorPosts', params)
      posts.forEach(post => this.posts.push(post))
      this.cursor = cursor
      this.loadingPosts = false
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.published-posts-view
  max-width: 900px
  margin: $baseline auto
</style>
