<template>
  <MyPosts>
    <PostWrapper
      v-for="post in posts"
      :post="post"
      :isSubscribed="true"
      :key="post.id"
    >
      <template #controls>
        <button-icon
          class="edit"
          v-b-tooltip
          :title="$t('Edit post')"
          @click.prevent="$router.push(`/posts/${post.id}`)"
        />
      </template>
    </PostWrapper>

    <div v-if="!posts.length && !loadingPosts" class="my-posts--empty">
      <p>{{ $t("You didn't publish any post.") }}</p>
    </div>

    <loading-spinner v-if="loadingPosts"></loading-spinner>
  </MyPosts>
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

      const params = {
        cursor: this.cursor,
        skipRecommendations: 1
      }
      const { posts, cursor } = await this.$axios.$get(
        `/authors/${this.user.id}/posts`, {params})

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
//- Empty placeholder
.my-posts--empty
  display: block
  margin: $baseline 0
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center
</style>
