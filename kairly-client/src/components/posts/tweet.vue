<template>
  <post :post="post">
    <timeline-post--tweet>
      <p v-html="post.content.content"></p>
      <tweet-attachment v-for="item in post.content.attachments" :item="item" :key="item.id || item.href" />
    </timeline-post--tweet>

    <template slot="extendedControls">
      <slot name="extendedControls">
        <a :href="post.source" class="tweet" v-tooltip.top="'Original tweet'"></a>
      </slot>
    </template>

    <template slot="controls"><slot name="controls"></slot></template>
  </post>
</template>

<script>

import post from './post';
import TweetAttachment from './TweetAttachment'

export default {
  name: 'post-tweet',

  props: ["post", "isSubscribed"],

  components: {
    post,
    TweetAttachment
  },
}
</script>

<style lang="sass">
timeline-post--tweet
  display: block
  margin-bottom: $baseline / 2

  font-family: $ff-serif
  font-size: $fs-1

  a
    color: $c-base

  //- picture
  img
    display: block
    margin-top: $baseline / 2
    max-width: 100%
</style>
