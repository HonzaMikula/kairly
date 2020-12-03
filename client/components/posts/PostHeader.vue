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
    post: { type: Object, required: true },
  },
}
</script>

<style lang="sass">
.box-header
  @media (max-width: $mobile)
    margin: $baseline/2 0 $baseline 0

  .is-selected & h2
    background: lighten($c-base, 40%)
    box-shadow: 0 0 6px $c-base

  h2
    position: relative
    display: grid
    align-items: center
    grid-template-columns: 1fr auto 1fr

    margin: $baseline 0 $baseline/2 0

    font-family: $ff-serif
    font-size: $fs-1
    text-align: center

    &::after,
    &::before
      height: 1px
      margin: 0 $baseline

      background: #ddd

      content: ''

      @media (max-width: $mobile)
        margin: 0 $baseline/2

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
