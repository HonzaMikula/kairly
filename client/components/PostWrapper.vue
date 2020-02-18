<template>
  <section class="normal-post">
    <component
      :is="postType"
      class="post-content"
      :post="post"
    >
      <template #author>
        <slot name="author"></slot>
      </template>

      <template #global-controls>
        <slot name="global-controls" :post="post"></slot>
      </template>

      <template #page-controls>
        <slot name="page-controls" :post="post"></slot>
      </template>
    </component>

    <slot name="aside">
    </slot>
  </section>
</template>

<script>
import PostArticle from '@/components/posts/PostArticle'
import PostComment from '@/components/posts/PostComment'
import PostLink from '@/components/posts/PostLink'
import PostTweet from '@/components/posts/PostTweet'
import PostPicture from '@/components/posts/PostPicture'
import PostVideo from '@/components/posts/PostVideo'
import PostRecommendations from '@/components/posts/PostRecommendations'

export default {
  name: 'PostWrapper',
  props: {
    post: Object,
  },

  components: {
    PostArticle,
    PostComment,
    PostLink,
    PostTweet,
    PostPicture,
    PostVideo,
    PostRecommendations,
  },

  computed: {
    postType() {
      if (this.post.type === 'newspaper') {
        return 'post-article'
      } else {
        return 'post-' + this.post.type
      }
    }
  }
}
</script>

<style lang="sass">
.normal-post
  position: relative

  .post
    border: 1px solid #eee
    box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff
</style>

