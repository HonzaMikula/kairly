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
            @click="moveTweetUp(idx)"
          />
          <button-icon
            v-if="idx < tweets.length - 1"
            class="down"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move tweet down')"
            @click="moveTweetDown(idx)"
          />
          <button-icon
            class="remove"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Remove tweet')"
            @click="removeTweetFromEditorial(tweet)"
          />
        </template>
      </PostTweet>
    </template>
    <template v-else>
      <div class="editorial-post-tweet-editor--empty">
        <h2>{{ $t('Add tweets here') }}</h2>
      </div>
    </template>

    <portal to="modal">
      <TweetsSelection
        :newspaper="newspaper"
        :selected="tweets.map(post => post.id)"
        @add="addTweetToEditorial"
        @remove="removeTweetFromEditorial"
        @done="$emit('done')"
      />
    </portal>
  </div>
</template>

<script>
import Vue from 'vue'

import PostTweet from '@/components/posts/PostTweet'
import TweetsSelection from '@/components/editor/backlog/TweetsSelection'

export default {
  name: 'EditorialTweetsEditor',

  components: {
    PostTweet,
    TweetsSelection,
  },

  props: {
    editorial: Object,
    newspaper: Object,
  },

  data() {
    return {
      tweets: this.editorial ? [...this.editorial.tweets] : []
    }
  },

  methods: {
    addTweetToEditorial(post) {
      this.tweets.push(post)
      this.saveEditorial()
      this.$store.commit('backlog/remove', {
        fullName: this.newspaper.fullName,
        source: 'considered',
        postId: post.id,
      })
    },

    removeTweetFromEditorial(post) {
      const idx = this.tweets.findIndex(p => p.id === post.id)
      this.tweets.splice(idx, 1)
      this.saveEditorial()
      this.$store.commit('backlog/append', {
        fullName: this.newspaper.fullName,
        source: 'considered',
        post: {post, editorial: null, publish: null},
      })
    },

    moveTweetDown(idx) {
      const { tweets } = this
      const tweet = tweets[idx]
      Vue.set(tweets, idx, tweets[idx + 1])
      Vue.set(tweets, idx + 1, tweet)
      this.saveEditorial()
    },

    moveTweetUp(idx) {
      const { tweets } = this
      const tweet = tweets[idx]
      Vue.set(tweets, idx, tweets[idx - 1])
      Vue.set(tweets, idx - 1, tweet)
      this.saveEditorial()
    },

    saveEditorial() {
      this.$emit('save', {
        type: 'tweets',
        tweets: this.tweets.map(t => t.id),
      })
    },
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
