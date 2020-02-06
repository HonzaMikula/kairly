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
  },
}
</script>

<style lang="sass">
.box-wrapper
  display: flex

  > *
    flex: 1

  .box-column.editorial
    background: #f2ecec
</style>
