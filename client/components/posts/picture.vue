<template>
  <post :post="post">
    <timeline-post--picture>
      <figure>
        <img :src="post.content.picture" :alt="post.content.title" />

        <figcaption>{{ post.content.title }}</figcaption>
      </figure>
    </timeline-post--picture>
    <template slot="controls"><slot name="controls"></slot></template>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-picture',
  props: ["post", "isSubscribed"],
  components: { post }
}
</script>

<style lang="sass">
timeline-post--picture
  display: block

  //- Title
  h2
    display: block
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600

  //- Picture
  img
    display: block
    margin-bottom: $baseline / 2
    height: 450px
    width: 100%

    object-fit: cover

  //- Figcaption
  figcaption
    display: block

    color: #999

    font-size: $fs--1
    font-family: $ff-serif
</style>
