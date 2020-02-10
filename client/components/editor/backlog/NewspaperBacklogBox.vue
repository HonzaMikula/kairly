<template>
  <compotent
    :is="Array.isArray(post) ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    :isSubscribed="true"
  >

  </compotent>
</template>

<script>
import PostWrapper from '@/components/PostWrapper'
import BoxWrapper from '@/components/BoxWrapper'

export default {
  name: 'NewspaperBacklogBox',

  components: {
    PostWrapper,
    BoxWrapper
  },

  // data() {
  //   return {
  //     editorType: null,
  //     editorPosition: null,
  //     mobileControls: false
  //   }
  // },

  props: {
    newspaper: Object,
    post: [Object, Array],
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: String,
  }
}
</script>
