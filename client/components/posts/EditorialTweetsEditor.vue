<template>
  <div 
    class="editorial-post-tweet-editor"
    :class="{'many-tweets': tweets.length > 1}">
    <template v-if="tweets.length">
      <PostTweet v-for="tweet in tweets" :key="tweet.id" :post="tweet">
        <template slot="extendedControls">&nbsp;</template>
        <template slot="controls">
          <button-icon
            class="up"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move tweet up')"
          />
          <button-icon
            class="down"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move tweet down')"
          />
          <button-icon
            class="remove"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Remove tweet')"
            @click="$emit('removeTweet', tweet)"
          />
        </template>
      </PostTweet>
    </template>
    <template v-else>
      Add tweets here.
    </template>
  </div>
</template>

<script>
import PostTweet from './PostTweet'

export default {
  name: 'EditorialTweetsEditor',

  components: {
    PostTweet
  },

  props: {
    tweets: Array
  },

  methods: {
  }

}
</script>
<style lang="sass">
.editorial-post-tweet-editor
  display: flex
  flex-direction: column
  justify-content: space-around

  background: #F2ECEC

  &.many-tweets
    align-self: start !important

  .post.tweet
    background: #F2ECEC
  
</style>
