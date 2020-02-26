<template>
  <PostBase :post="post">
    <div class="post-body">
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <nuxt-link v-else :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link>
      </h2>

      <div class="post-body--content">
        <div v-html="post.content.content"></div>
      </div>
    </div>

    <template #page-controls><slot name="page-controls"></slot></template>
    <template #global-controls><slot name="global-controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'PostComment',

  props: {
    post: Object,
  },

  components: {
    PostBase
  }
}
</script>


<style lang="sass">
@import './styles/components/article-perex'


.comment > .post-body
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
.comment .post-body--content
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


.editorial-post
  .timeline-post--comment--content
    column-count: 2

// HACK by farin
.post-content.comment time
    visibility: hidden

</style>
