<template>
  <PostBase :post="post">
    <div class="timeline-post--tweet">
      <!-- p tag is not allowed here because content can cointains other <p>
          (eg extrnal url). And it brokes hydrating server side rendered page-->
      <div class="tweet-content" v-html="post.content.content" />

      <template v-if="photoAttachments">
        <TweetAttachmentPhoto :items="photoAttachments" />
      </template>

      <template v-if="otherAttachments">
        <component
          :is="'tweet-attachment-' + attachmentType(attachment.type)"
          v-for="attachment in otherAttachments"
          :key="attachment.id"
          :item="attachment"
        />
      </template>
    </div>

    <template #global-controls>
      <slot name="global-controls">
        <a
          v-if="post.source"
          v-b-tooltip
          :href="post.source"
          target="_blank"
          class="tweet"
          :title="$t('Original tweet')"
        />
      </slot>
    </template>

    <template #page-controls><slot name="page-controls" /></template>
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
  name: 'PostTweet',

  components: {
    PostBase,
    TweetAttachmentLink,
    TweetAttachmentPhoto,
    TweetAttachmentQuote,
    TweetAttachmentVideo,
    TweetAttachmentGif
  },

  props: {
    post: Object,
  },

  computed: {
    photoAttachments () {
      if (this.post.content.attachments) {
        const photoAttachments = this.post.content.attachments.filter(attachment => attachment.type === 'media.photo')

        if (photoAttachments.length > 0) { return photoAttachments }
      }
      return false
    },

    otherAttachments () {
      if (this.post.content.attachments) {
        const otherAttachments = this.post.content.attachments.filter(attachment => attachment.type !== 'media.photo')

        if (otherAttachments.length > 0) { return otherAttachments }
      }
      return false
    }
  },

  methods: {
    attachmentType (type) {
      switch (type) {
        case 'media.photo':
          return 'photo'
        case 'media.animated_gif':
          return 'gif'
        case 'media.video':
          return 'video'
        case 'url':
          return 'link'
        case 'quoted_status':
          return 'quote'
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
    word-break: break-word
</style>
