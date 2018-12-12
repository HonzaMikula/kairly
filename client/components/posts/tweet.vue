<template>
  <post :post="post">
    <timeline-post--tweet>
      <!-- p tag is not allowed here because content can cointains other <p>
          (eg extrnal url). And it brokes hydrating server side rendered page-->
      <div class="tweet-content" v-html="post.content.content"></div>

      <component
        v-if="post.content.attachments"
        :is="'tweet-attachment-' + attachmentType"
        :items="post.content.attachments"
        :key="post.id"
      />

    </timeline-post--tweet>

    <template slot="extendedControls">
      <slot name="extendedControls">
        <a
          v-if="post.source"
          :href="post.source"
          target="_blank"
          class="tweet"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
          :title="$t('Original tweet')">
        </a>
      </slot>
    </template>

    <template slot="controls"><slot name="controls"></slot></template>
  </post>
</template>

<script>

import post from './post'
import TweetAttachmentGif from './TweetAttachmentGif'
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
    TweetAttachmentVideo,
    TweetAttachmentGif
  },

  computed: {
    attachmentType() {
      switch (this.post.content.attachments[0].type) {
        case "media.photo":
          return "photo"
          break
        case "media.animated_gif":
          return "gif"
          break
        case "media.video":
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
  line-height: 1.58

  @media (max-width: $mobile)
    font-size: $fs--1

  > .tweet-content a
    color: $c-base
</style>
