<template>
  <post-wrapper
    :post="post.ref"
    :isSubscribed="isSubscribed"
  />
</template>

<script>
import post from './post';

export default {
  name: 'post-recommendation-post',

  props: ["post", "isSubscribed"],

  // resolve circular component dependency
  // https://vuejs.org/v2/guide/components-edge-cases.html#Circular-References-Between-Components
  components: {
    PostWrapper: () => import('@/components/PostWrapper')
  }
}
</script>

<style lang="sass">
</style>
