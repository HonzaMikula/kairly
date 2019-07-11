<template>
  <div class="editorial-post--editorial">
    <PostTweet v-for="tweet in editorial.tweets" :key="tweet.id" :post="tweet" />
  </div>
</template>



<script>
// Docs
// - component is for distinguishing tweets, article, writing article, selecting tweets
//

import PostTweet from './PostTweet'

export default {
  name: 'EditorialTweets',

  components: {
    PostTweet
  },

  props: {
    editorial: Object
  }
}
</script>
<style lang="sass">
</style>
