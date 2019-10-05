<template>
  <PostBase :post="post">
    <div class="timeline-post--tweet">
      <!-- p tag is not allowed here because content can cointains other <p>
          (eg extrnal url). And it brokes hydrating server side rendered page-->
      <div class="tweet-content" v-html="post.content.content"></div>

      <template v-if="photoAttachments">
        <TweetAttachmentPhoto :items="photoAttachments" />
      </template>
      
      <template v-if="otherAttachments">
        <component
          v-for="attachment in otherAttachments"
          :is="'tweet-attachment-' + attachmentType(attachment.type)"
          :item="attachment"
          :key="attachment.id"
        />
      </template>
    </div>

    <template #extended-controls>
      <slot name="extended-controls">
        <a
          v-if="post.source"
          :href="post.source"
          target="_blank"
          class="tweet"
          v-b-tooltip
          :title="$t('Original tweet')">
        </a>
      </slot>
    </template>

    <template #controls><slot name="controls"></slot></template>
  </PostBase>
</template>

<script>

import PostBase from './PostBase'
import TweetAttachmentGif from './TweetAttachmentGif'
import TweetAttachmentLink from './TweetAttachmentLink'
import TweetAttachmentPhoto from './TweetAttachmentPhoto'
import TweetAttachmentQuote from './TweetAttachmentQuote'
import TweetAttachmentVideo from './TweetAttachmentVideo'

export default {
  name: 'post-tweet',

  props: ["post", "isSubscribed"],

  components: {
    PostBase,
    TweetAttachmentLink,
    TweetAttachmentPhoto,
    TweetAttachmentQuote,
    TweetAttachmentVideo,
    TweetAttachmentGif
  },

  computed: {
    photoAttachments() {
      if (this.post.content.attachments) {
        const photoAttachments = this.post.content.attachments.filter(attachment => attachment.type == 'media.photo')
        
        if (photoAttachments.length > 0)
          return photoAttachments
      }
      return false
    },

    otherAttachments() {
      if (this.post.content.attachments) {
        const otherAttachments = this.post.content.attachments.filter(attachment => attachment.type != 'media.photo')

        if (otherAttachments.length > 0)
          return otherAttachments
      }
      return false
    }
  },

  methods: {
    attachmentType(type) {
      switch (type) {
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
.timeline-post--tweet
  display: block

  font-family: $ff-serif
  line-height: 1.6
  font-size: 15px

  > .tweet-content a
    color: $c-base
</style>
