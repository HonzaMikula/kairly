<template>
  <component
    :is="'post-' + postType"
    :key="post.id"
    :post="post"
    :isSubscribed="isSubscribed"
    :editorial="editorial"
  >
    <template slot="author">
      <slot name="author"></slot>
    </template>

    <template slot="extendedControls">
      <slot name="extendedControls"></slot>
    </template>

    <template slot="controls">
      <slot name="controls"></slot>
    </template>
  </component>
</template>

<script>
import PostArticle from '@/components/posts/PostArticle'
import PostLink from '@/components/posts/PostLink'
import PostTweet from '@/components/posts/PostTweet'
import PostPicture from '@/components/posts/PostPicture'
import PostRecommendations from '@/components/posts/PostRecommendations'
import PostEditorial from '@/components/posts/Editorial'

export default {
  name: 'PostWrapper',
  props: ['post', 'isSubscribed', 'editorial'],

  components: {
    PostArticle,
    PostLink,
    PostTweet,
    PostPicture,
    PostRecommendations,
    PostEditorial
  },

  computed: {
    //- TEMP hack - we can get rid of it after migration
    postType() {
      if (this.editorial == 'article' || this.editorial == 'tweet') {
        return 'editorial'
      }
      else if (this.post.type == 'newspaper') {
        return 'article' // TODO: back to 'article'
      }
      else {
        return this.post.type
      }
    }
  }
}
</script>
