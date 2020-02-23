<template>
  <section class="post-wrapper">
    <component
      :is="postType"
      class="post-content"
      :post="post"
      @close-editor="p => $emit('close-editor', p)"
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
import PostHeader from '@/components/posts/PostHeader'
import PostLink from '@/components/posts/PostLink'
import PostTweet from '@/components/posts/PostTweet'
import PostPicture from '@/components/posts/PostPicture'
import PostVideo from '@/components/posts/PostVideo'
import PostRecommendations from '@/components/posts/PostRecommendations'

export default {
  name: 'PostWrapper',
  props: {
    post: Object,
    typeOverride: Object // override component type is set, value is map {id: component}
  },

  components: {
    PostArticle,
    PostComment,
    PostHeader,
    PostLink,
    PostTweet,
    PostPicture,
    PostVideo,
    PostRecommendations,
  },

  computed: {
    postType() {
      if (this.typeOverride) {
        const component = this.typeOverride[this.post.id]
        if (component) {
          return component
        }
      }
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
.post-wrapper
  position: relative

  //- in backlog the margin is done by the toolbar
  &:first-of-type > article,
  .newspaper-backlog-post-toolbar-view + & > article
    margin-bottom: 0

  > article
    box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff
</style>

