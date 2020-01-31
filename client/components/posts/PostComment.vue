<template>
  <PostBase :post="post">
    <timeline-post--comment>
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <nuxt-link v-else :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link>
      </h2>

      <timeline-post--comment--content>
        <div v-html="post.content.content"></div>
      </timeline-post--comment--content>
    </timeline-post--comment>

    <template #controls><slot name="controls"></slot></template>
    <template #extended-controls><slot name="extended-controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'PostComment',

  props: ["post", "isSubscribed"],

  components: {
    PostBase
  }
}
</script>


<style lang="sass">
@import './styles/components/article-perex'


timeline-post--comment
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
timeline-post--comment--content
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


// HACK by farin
.post-content.comment time
    visibility: hidden

</style>
