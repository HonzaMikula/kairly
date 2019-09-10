<template>
  <div class="tweets-selection-view">
    <header>
      <h2>Select tweets</h2>

      <button
        @click="$emit('done')"
      >Done</button>
    </header>
    <PostTweet v-for="post in tweets" :post="post" :key="post.id">
      <template #extended-controls>
        &nbsp;
      </template>
      <template #controls>
        <button
          v-if="selected.indexOf(post.id) === -1"
          class="add"
          @click="$emit('add', post)"
        />
        <button
          v-else
          class="remove"
          @click="$emit('remove', post)"
        />
      </template>
    </PostTweet>
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

  computed: {
    tweets() {
      const { considered } = this.$store.state.newspaperBacklog[this.newspaper.fullName]
      return considered.map(log => log.post).filter(post => post.type === 'tweet')
    },
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.tweets-selection-view
  position: fixed
  right: $baseline
  top: 10vh

  max-height: 80vh
  overflow: auto
  width: 300px

  background: #fff
  box-shadow: 0 0 7px rgba(0,0,0,0.5)

  //- Header
  > header
    display: grid
    grid-template-columns: auto min-content
    padding: $baseline/4

    border-bottom: 1px solid #eee

    //- heading
    h2
      font-weight: 600

    //- done button
    button
      +button(primary, small)
</style>
