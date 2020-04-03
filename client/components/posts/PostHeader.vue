<template>
  <div class="box-header">
    <h2 v-if="post.title">{{ post.title }}</h2>
    <hr v-else>
  </div>
</template>

<script>

export default {
  name: 'PostHeader',

  props: {
    post: Object,
  }
}
</script>

<style lang="sass">
.box-header
  @media (max-width: $mobile)
    border-bottom: 1px solid #ddd
    margin: $baseline/2 0 $baseline 0

  h2
    position: relative
    margin: $baseline 0 $baseline/2 0
    font-family: $ff-serif
    font-size: $fs-1
    text-align: center

    @media (max-width: $mobile)
      position: relative
      top: $baseline / 2

      display: table
      margin: 0 auto
      padding: 0 $baseline/2

      background: #fafafa

    &::after,
    &::before
      position: absolute
      left: $baseline * 2
      top: $baseline / 2
      width: 25%
      border-top: 1px solid #ddd
      content: ''

      @media (max-width: $mobile)
        display: none

    &::after
      right: $baseline * 2
      left: auto

  hr
    height: 1px
    margin: $baseline $baseline*2
    color: #ddd
    background: #ddd
    border: 0

    @media (max-width: $mobile)
      display: none
</style>
