<template>
  <div
    :class="`box-wrapper ${css}`"
  >
    <div
      v-for="(col, idx) in columns"
      :key="idx"
      :class="`box-column ${col.css}`"
    >
      <PostWrapper
        v-for="(post, postIdx) in col.posts"
        :key="postIdx"
        :post="post"
        :isSubscribed="true"
      />
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
    post: Array,
  },

  components: {
    PostWrapper,
  },

  computed: {
    css() {
      return isString(this.post[0]) ? this.post[0] : null
    },

    columns() {
      let cols = isString(this.post[0]) ? this.post.slice(1) : this.post
      return cols.map(c => {
        return {
          css: isString(c[0]) ? c[0] : '',
          posts: isString(c[0]) ? c.slice(1) : c
        }
      })
    }
  }
}
</script>

<style lang="sass">
.box-wrapper
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
