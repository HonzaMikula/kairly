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
        :typeOverride="typeOverride"
        @close-editor="p => $emit('close-editor', p)"
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
    typeOverride: Object // override component type is set, value is map {id: component}
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

    //- 1st column
    .box-column:nth-of-type(1)
      .post-body--content
        columns: 2

    //- 2nd column
    .box-column:nth-of-type(2)
      .post-body--content
        columns: 1

  &.cols-1-2
    grid-template-columns: 1fr 2fr

    @media (max-width: $mobile)
      grid-template-columns: 60vw calc(100vw - (#{$baseline} * 1.5))

      overflow: auto
      scroll-behavior: smooth
      -webkit-overflow-scrolling: touch

    //- 1st column
    .box-column:nth-of-type(1)
      .post-body--content
        columns: 1

    //- 2nd column
    .box-column:nth-of-type(2)
      .post-body--content
        columns: 2

  &.cols-1-1
    grid-template-columns: 1fr 1fr

    .newspaper .post-body--content,
    .comment .post-body--content
      columns: 2

  &.cols-1-1-1
    grid-template-columns: 1fr 1fr 1fr

    .newspaper .post-body--content,
    .comment .post-body--content
      columns: 1

.box-column.editorial
  position: relative
  left: 1px
  background: #f2ecec
</style>
