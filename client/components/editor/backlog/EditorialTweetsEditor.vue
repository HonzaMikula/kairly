<template>
  <div
    class="editorial-post-tweet-editor"
    :class="{'many-tweets': tweets.length > 1}">
    <template v-if="tweets.length">
      <PostTweet v-for="(tweet, idx) in tweets" :key="tweet.id" :post="tweet">
        <template #extended-controls>&nbsp;</template>
        <template #controls>
          <button-icon
            v-if="idx > 0"
            class="up"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move tweet up')"
            @click="$emit('moveTweetUp', tweet)"
          />
          <button-icon
            v-if="idx < tweets.length - 1"
            class="down"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move tweet down')"
            @click="$emit('moveTweetDown', tweet)"
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

    <portal to="modal">
      <TweetsSelection :newspaper="newspaper"/>
    </portal>
  </div>
</template>

<script>
import PostTweet from '@/components/posts/PostTweet'
import TweetsSelection from '@/components/editor/backlog/TweetsSelection'

export default {
  name: 'EditorialTweetsEditor',

  components: {
    PostTweet,
    TweetsSelection,
  },

  props: {
    newspaper: Object,
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

  .tweet-attachment-link-view
    display: none //- TODO: refactor so it's not done over CSS

//- If no tweets
.editorial-post-tweet-editor--empty
  padding: $baseline/2

  color: #555

  h2
    font-size: $fs-1
    font-weight: 600


</style>
