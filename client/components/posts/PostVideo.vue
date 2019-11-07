<template>
  <PostBase :post="post">
    <div class="timeline-post--video">
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <nuxt-link v-else :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link>
      </h2>

      <div class="timeline-post--video--content">
        <div v-html="post.content.perex"></div>
        <div v-if="poster">
          <img :src="poster.src" />
        </div>
      </div>
    </div>

    <template #controls><slot name="controls"></slot></template>
    <template #extended-controls><slot name="extended-controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'PostVideo',

  props: ["post", "isSubscribed"],

  components: {
    PostBase
  },

  computed: {
    poster() {
      if (this.post.content.attachments) {
        const posterAttachments = this.post.content.attachments.filter(attachment => attachment.type == 'video-poster')

        if (posterAttachments.length > 0)
          return posterAttachments[0]
      }
      return null
    },
  },
}
</script>

<style lang="sass">
@import './styles/components/article-perex'

.timeline-post--video
  font-family: $ff-serif

  //- Title
  > h2
    display: block
    margin-bottom: $baseline / 4

    font-size: $fs-1
    font-weight: 600
    line-height: 1.58

    @media (max-width: $mobile)
      font-size: $fs-0

    a
      color: #000

  a
    color: $c-base

//- Content
.timeline-post--video--content
  position: relative

  column-count: 3
  column-rule: 1px dotted #ddd
  column-gap: $baseline
  display: block

  line-height: 1.58
  hyphens: auto

  @media (max-width: $mobile)
    column-count: 2
    column-gap: $baseline / 2

    font-size: 15px
    line-height: 1.58


  +article-perex
</style>
