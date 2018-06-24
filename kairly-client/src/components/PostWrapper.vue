<template>
  <component
    :is="'post-' + post.type"
    :post="post"
    :isSubscribed="isSubscribed"
    :key="post.id"
  >
    <template slot="controls">
      <slot name="controls"></slot>
    </template>
  </component>
</template>

<script>
import postNewspaper from '@/components/posts/newspaper'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'PostWrapper',
  props: ['post', 'isSubscribed'],

  components: {
    postNewspaper,
    postTweet,
    postPicture,
  }
}
</script>
