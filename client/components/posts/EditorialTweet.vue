<template>
  <div class="editorial-post--editorial">
    <PostTweet v-for="tweet in tweets" :key="tweet.id" :post="tweet" />
  </div>
</template>



<script>
// Docs
// - component is for distinguishing tweets, article, writing article, selecting tweets
//
import TWEETS from '@/tempDataTweets'
import PostTweet from './PostTweet'

export default {
  name: 'EditorialTweet',

  components: {
    PostTweet
  },

  data() {
    return {
      tweets: TWEETS
    }
  }
}
</script>
<style lang="sass">
</style>
