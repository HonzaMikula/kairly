<template>
  <post :post="post">
    <timeline-post--tweet>
      <p v-html="post.content.content"></p>
      <img :src="post.content.picture" v-if="post.content.picture" />
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

  .external-url
    margin-top: 5px
    padding: 5px 10px
    background-color: #fafafa

  .external-url--title
    font-size: $fs-0

  .external-url--netloc
    font-size: $fs--2
    color: #888


</style>
