<template>
  <div class="box-header">
    <h2 v-if="post.title">{{ post.title }}</h2>
    <hr v-else />
  </div>
</template>

<script>

export default {
  name: 'post-header',

  props: {
    post: Object,
  }
}
</script>

<style lang="sass">
.box-header
  h2
    position: relative
    margin: $baseline 0 $baseline/2 0
    font-family: $ff-serif
    font-size: $fs-1
    text-align: center

    &::after,
    &::before
      position: absolute
      left: $baseline * 2
      top: $baseline / 2
      width: 25%
      border-top: 1px solid #ddd
      content: ''

    &::after
      right: $baseline * 2
      left: auto

  hr
    margin: $baseline $baseline*2
    border-top: 1px solid #ddd
</style>
