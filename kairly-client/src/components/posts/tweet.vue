<template>
  <post :post="post">
    <timeline-post--tweet>
      <p v-html="post.content.content"></p>
      <img :src="post.content.picture" v-if="post.content.picture" />
    </timeline-post--tweet>
    <template slot="controls"><slot name="controls"></slot></template>
  </post>
</template>

<script>

import post from './post';

export default {
  name: 'post-tweet',
  props: ["post", "isSubscribed"],
  components: { post },
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
