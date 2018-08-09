<template>
  <post :post="post">
    <timeline-post--tweet>
      <p v-html="post.content.content"></p>

      <component
        v-if="post.content.attachments"
        :is="'tweet-attachment-' + attachmentType"
        :items="post.content.attachments"
        :key="post.id"
      />

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
import TweetAttachmentLink from './TweetAttachmentLink'
import TweetAttachmentPhoto from './TweetAttachmentPhoto'
import TweetAttachmentQuote from './TweetAttachmentQuote'
import TweetAttachmentVideo from './TweetAttachmentVideo'

export default {
  name: 'post-tweet',

  props: ["post", "isSubscribed"],

  components: {
    post,
    TweetAttachmentLink,
    TweetAttachmentPhoto,
    TweetAttachmentQuote,
    TweetAttachmentVideo
  },

  computed: {
    attachmentType() {
      switch (this.post.content.attachments[0].type) {
        case "media.photo":
          return "photo"
          break
        case "media.animated_gif":
          return "video"
          break
        case "url":
          return "link"
          break
        case "quoted_status":
          return "quote"
          break
      }
    }
  }
}
</script>

<style lang="sass">
timeline-post--tweet
  display: block
  margin-bottom: $baseline / 2

  font-family: $ff-serif
  line-height: $baseline * 0.9

  > p a
    color: $c-base
</style>
