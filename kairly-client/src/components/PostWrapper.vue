<template>
  <component
    :is="'post-' + postType"
    :post="post"
    :isSubscribed="isSubscribed"
    :key="post.id"
  >
    <template slot="extendedControls">
      <slot name="extendedControls"></slot>
    </template>

    <template slot="controls">
      <slot name="controls"></slot>
    </template>
  </component>
</template>

<script>
import postArticle from '@/components/posts/article'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'PostWrapper',
  props: ['post', 'isSubscribed'],

  components: {
    postArticle,
    postTweet,
    postPicture,
  },

  computed: {
    //- TEMP hack - we can get rid of it after migration
    postType() {
      if (this.post.type == 'newspaper') {
        return 'article'
      }
      else {
        return this.post.type
      }
    }

  }
}
</script>
