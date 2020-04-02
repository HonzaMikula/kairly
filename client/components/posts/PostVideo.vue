<template>
  <PostBase :post="post">
    <div class="post-video-view">
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <a :href="post.source" target="_blank">{{ post.content.title }}</a>
      </h2>

      <div class="post-video--content">
        <div
          v-if="poster"
          class="post-video--content--player"
        >
          <a :href="post.source" target="_blank">
            <img :src="poster.src" />
          </a>
        </div>

        <div class="post-video--content--perex">
          <div v-html="post.content.perex"></div>

          <div class="post-video--content--perex--watch-video">
            <a :href="post.source" target="_blank">
              {{ $t('Watch video') }}
            </a>
          </div>
        </div>
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

  props: {
    post: Object,
  },

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
@import './styles/mixins/perex-button'

.post-video-view
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
.post-video--content
  display: grid
  grid-template-columns: 2fr 1fr
  grid-column-gap: $baseline

  @media (max-width: $mobile)
    grid-template-columns: 1fr

  .cols-1-1-1 &,
  .cols-2-1 &,
  .cols-1-2 &,
  .cols-1-1 &
    grid-template-columns: 1fr

    .post-video--content--perex--watch-video
      display: none

.post-video--content--player
  a
    position: relative
    display: block

    &::before
      +fa-icon()
      @extend .fas

      position: absolute
      left: 50%
      top: 50%

      color: #fff
      opacity: 0.7

      font-size: 40px

      transform: translate(-50%, -50%)
      transition: opacity 0.2s
      content: fa-content($fa-var-play)

    &:hover,
    &:focus
      &::before
        opacity: 1

  img
    height: auto
    width: 100%

.post-video--content--perex
  font-size: 15px
  word-break: break-word
  line-height: 1.6

.post-video--content--perex--watch-video
  +perex-button
</style>
