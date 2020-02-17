<template>
  <PostBase :post="post">
    <div class="timeline-post--video">
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <a :href="post.source" target="_blank">{{ post.content.title }}</a>
      </h2>

      <div class="timeline-post--video--content">
        <div
          v-if="poster"
          class="timeline-post--video--content--player"
        >
          <a :href="post.source" target="_blank">
            <img :src="poster.src" />
          </a>
        </div>

        <div v-html="post.content.perex"></div>

      </div>
    </div>

    <template #page-controls><slot name="page-controls"></slot></template>
    <template #global-controls><slot name="global-controls"></slot></template>
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
  display: grid
  grid-template-columns: 2fr 1fr
  grid-column-gap: $baseline

  @media (max-width: $mobile)
    grid-template-columns: 1fr


.timeline-post--video--content--player
  img
    height: auto
    width: 100%
</style>
