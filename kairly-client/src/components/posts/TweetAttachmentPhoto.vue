<template>
  <tweet-attachment-gallery :class="'gallery-'+ items.length">
    <img v-for="item in items" :key="item.href" :src="`${item.src}:small`" :width="item.sizes.small.w" :height="item.sizes.small.h" />
  </tweet-attachment-gallery>
</template>

<script>
export default {
  name: 'tweet-attachment-photo',

  props: ["items"]
}
</script>

<style lang="sass">
tweet-attachment-gallery
  display: grid
  grid-column-gap: 2px
  grid-row-gap: 2px
  height: 383px
  margin-bottom: -($baseline/2)
  margin-top: $baseline / 2

  &.gallery-1
    grid-template-columns: 1fr
    grid-template-rows: 1fr

  &.gallery-2
    grid-template-columns: 1fr 1fr
    grid-template-rows: 1fr

  &.gallery-3
    grid-template-columns: 1fr 1fr
    grid-template-rows: 1fr 1fr

    img:nth-of-type(2)
      grid-column: 2 / span 1
      grid-row: 1 / span 2

  &.gallery-4
    grid-template-columns: 1fr 1fr
    grid-template-rows: 1fr 1fr

  img
    object-fit: cover
    width: 100%
    height: 100%

</style>
