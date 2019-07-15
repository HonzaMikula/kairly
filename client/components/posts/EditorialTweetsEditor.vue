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
      <div class="editorial-post-tweet-editor--empty">
        <h2>Add tweets here</h2>
        <p>Check the right column and click on Add to Editorial.</p>
      </div>
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

  //- if many tweets, align to top
  &.many-tweets
    align-self: start !important

  .post.tweet
    background: #F2ECEC

  tweet-attachment-link-view
    display: none //- TODO: refactor so it's not done over CSS
  
//- If no tweets
.editorial-post-tweet-editor--empty
  padding: $baseline/2

  color: #555

  h2
    font-size: $fs-1
    font-weight: 600

  
</style>
