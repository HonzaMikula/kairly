<template>
  <div class="tweet-attachment-gallery" :class="'gallery-'+ items.length">
    <a
      :href="`${item.src}:large`"
      v-for="item in items"
      :key="item.id"
      target="_blank">
      <img :src="`${item.src}:small`" :width="item.sizes.small.w" :height="item.sizes.small.h" />
    </a>
  </div>
</template>

<script>
export default {
  name: 'tweet-attachment-photo',

  props: ["items"]
}
</script>

<style lang="sass">
.tweet-attachment-gallery
  display: grid
  grid-column-gap: 2px
  grid-row-gap: 2px
  max-height: 383px
  margin-top: $baseline / 2

  &.gallery-1
    grid-template-columns: 100%
    grid-template-rows: minmax(auto, max-content)

    .cols-2-1 .box-column:nth-of-type(2) &,
    .cols-1-2 .box-column:nth-of-type(1) &
      img
        display: block
        height: auto
        max-height: 288px

        object-fit: contain

  &.gallery-2
    grid-template-columns: 50% 50%
    grid-template-rows: minmax(auto, max-content)

    .cols-2-1 .box-column:nth-of-type(2) &,
    .cols-1-2 .box-column:nth-of-type(1) &
      grid-template-columns: auto
      grid-template-rows: auto

      img
        display: block
        height: auto
        max-height: 288px

        object-fit: contain

  &.gallery-3
    grid-template-columns: 50% 50%
    grid-template-rows: minmax(auto, 191.5px) minmax(auto, 191.5px)
    
    .cols-2-1 .box-column:nth-of-type(2) &,
    .cols-1-2 .box-column:nth-of-type(1) &
      grid-template-columns: auto
      grid-template-rows: auto

      img
        display: block
        height: auto
        max-height: 288px

        object-fit: contain

    a:nth-of-type(2)
      grid-column: 2 / span 1
      grid-row: 1 / span 2

  &.gallery-4
    grid-template-columns: 50% 50%
    grid-template-rows: minmax(auto, 191.5px) minmax(auto, 191.5px)

    .cols-2-1 .box-column:nth-of-type(2) &,
    .cols-1-2 .box-column:nth-of-type(1) &
      grid-template-columns: auto
      grid-template-rows: auto

      img
        display: block
        height: auto
        max-height: 288px

        object-fit: contain

  img
    object-fit: cover
    width: 100%
    height: 100%

</style>
