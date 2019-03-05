<template>
  <div>
    ❤❤❤ Recommendation ❤❤❤

    <post-wrapper
      :post="post.ref"
      :isSubscribed="isSubscribed"
    />
  </div>
</template>

<script>
import post from './post';
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'post-recommendation-post',

  props: ["post", "isSubscribed"],

  components: {
    PostWrapper
  }
}
</script>

<style lang="sass">
</style>
