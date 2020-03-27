<template>
  <AppLayout :name="$t('Published posts')">
    <div class="published-posts-view">
      <PostWrapper
        v-for="post in posts"
        :post="post"
        :key="post.id"
      >
        <template #page-controls>
          <button-icon
            class="edit"
            v-b-tooltip
            :title="$t('Edit post')"
            @click.prevent="$router.push(`/posts/${post.id}`)"
          />
        </template>
      </PostWrapper>

      <div v-if="!posts.length && !loadingPosts" class="my-posts--empty">
        <h2>{{ $t('You haven\'t published any post yet.') }}</h2>

        <div class="draft-posts--empty--buttons">
          <nuxt-link to="/posts/create/article">{{ $t('Write an article') }}</nuxt-link>
          <nuxt-link to="/posts/create/tweet">{{ $t('Write a tweet') }}</nuxt-link>
        </div>
      </div>

      <loading-spinner v-if="loadingPosts"></loading-spinner>
    </div>
  </AppLayout>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'Drafts',

  components: {
    AppLayout,
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
  },

  created() {
    this.loadPosts()
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.published-posts-view
  max-width: 900px
  margin: $baseline auto

//- Empty placeholder
.published-posts--empty
  display: block
  margin: $baseline 0

  text-align: center

  h2 
    margin-bottom: $baseline / 2

    font-size: $fs-2
    font-weight: 600

  p
    margin-bottom: $baseline

.published-posts--empty--buttons
  display: flex
  justify-content: center

  a
    +button
    margin: 0 $baseline/4
</style>
