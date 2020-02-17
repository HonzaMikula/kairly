<template>
  <div
    :class="`box-wrapper ${post.css}`"
  >
    <div
      v-for="(col, colIndex) in post.columns"
      :key="colIndex"
      :class="`box-column ${col.css}`"
    >
      <PostWrapper
        v-for="(post, postIndex) in col.posts"
        :key="`${colIndex}-${post.id}`"
        :post="post"
        :isSubscribed="true"
      >
        <template #page-controls>
          <slot name="page-controls" :post="post" :postIndex="postIndex" :column="col" :columnIndex="colIndex"></slot>
        </template>
      </PostWrapper>

    </div>

    <slot name="aside">
    </slot>
  </div>
</template>

<script>
import isString from 'lodash/isString'

import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'BoxWrapper',
  props: {
    post: Object,
  },

  components: {
    PostWrapper,
  },
}
</script>

<style lang="sass">
.box-wrapper
  position: relative
  display: grid
  align-items: stretch
  margin-bottom: $baseline / 2

  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  .post
    margin-bottom: 0

    border: 0
    box-shadow: none
    background: transparent

  &.cols-2-1
    grid-template-columns: 2fr 1fr

    @media (max-width: $mobile)
      grid-template-columns: calc(100vw - (#{$baseline} * 1.5)) 60vw

      overflow: auto
      scroll-behavior: smooth
      -webkit-overflow-scrolling: touch

    timeline-post--article--content
      columns: 2

  &.cols-1-2
    grid-template-columns: 1fr 2fr

    @media (max-width: $mobile)
      grid-template-columns: 60vw calc(100vw - (#{$baseline} * 1.5))

      overflow: auto
      scroll-behavior: smooth
      -webkit-overflow-scrolling: touch

    timeline-post--article--content
      columns: 2

  &.cols-1-1
    grid-template-columns: 1fr 1fr

    timeline-post--article--content
      columns: 2

  &.cols-1-1-1
    grid-template-columns: 1fr 1fr 1fr

.box-column.editorial
  position: relative
  left: 1px
  background: #f2ecec
</style>
