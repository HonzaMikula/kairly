<template>
  <div class="tweets-selection-view">
    <header>
      <h2>{{ $t('Select tweets') }}</h2>

      <button @click="$emit('done')">
        {{ $t('Done') }}
      </button>
    </header>

    <main>
      <PostTweet v-for="post in tweets" :post="post" :key="post.id">
        <template #extended-controls>
          &nbsp;
        </template>
        <template #controls>
          <button
            v-if="selected.indexOf(post.id) === -1"
            class="add"
            @click="add(post)"
          />
          <button
            v-else
            class="remove"
            @click="remove(post)"
          />
        </template>
      </PostTweet>
    </main>
  </div>
</template>

<script>
import Vue from 'vue'

import { mapActions, mapMutations } from 'vuex'
import PostTweet from '@/components/posts/PostTweet'

export default {
  name: 'TweetsSelection',

  components: {
    PostTweet
  },

  props: {
    newspaper: Object,
    selected: Array
  },

  data() {
    const { considered } = this.$store.state.newspaperBacklog[this.newspaper.fullName]
    const tweets = considered.map(log => log.post).filter(post => post.type === 'tweet')
    return {
      alwaysDisplayTweets: tweets
    }
  },

  computed: {
    tweets() {
      // do not remove from tweets when tweet is moved from baclog to editorial
      // but add tweet to list when moved from editoril back to backlog
      const { considered } = this.$store.state.newspaperBacklog[this.newspaper.fullName]
      const backlogTweets = considered.map(log => log.post).filter(post => post.type === 'tweet')

      const ids = {}
      this.alwaysDisplayTweets.forEach(p => { ids[p.id] = true })

      const tweets = [...this.alwaysDisplayTweets]

      backlogTweets.forEach(p => {
        if (!ids[p.id]) {
          tweets.push(p)
          this.alwaysDisplayTweets.push(p)
        }
      })

      return tweets
    }
  },

  methods: {
    add(post) {
      this.$emit('add', post)
    },

    remove(post) {
      this.$emit('remove', post)
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.tweets-selection-view
  position: fixed
  right: $baseline
  top: 10vh

  display: grid
  grid-template-rows: $baseline * 1.5 1fr
  max-height: 80vh
  overflow: auto
  width: 300px

  background: #fff
  box-shadow: 0 0 7px rgba(0,0,0,0.5)

  @media (max-width: 1500px)
    right: 50%
    transform: translateX(45%)

  //- Header
  > header
    display: grid
    grid-template-columns: auto min-content
    padding: $baseline/4 $baseline/2

    border-bottom: 1px solid #eee

    //- heading
    h2
      font-weight: 600

    //- done button
    button
      +button(primary, small)

  //- Main
  main
    overflow: auto
</style>
