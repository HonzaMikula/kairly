<template>
  <div class="tweets-selection-view">
    <header>
      <h2>Select tweets</h2>

      <button>Done</button>
    </header>
    <PostTweet v-for="item in backlog" :post="item.post" :key="item.post.id">
      <template #extended-controls>
        &nbsp;
      </template>
      <template #controls>
        <button
          @click="selectTweet(item.post.id)"
          :class="{'add': !selectedTweets[item.post.id], 'remove': selectedTweets[item.post.id]}"
        >
        </button>
      </template>
    </PostTweet>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
import PostTweet from '@/components/posts/PostTweet'

export default {
  name: 'TweetsSelection',

  components: {
    PostTweet
  },

  props: {
    newspaper: Object,
  },

  data() {
    return {
      selectedTweets: [],
    }
  },

  computed: {
    backlog() {
      const { considered } = this.$store.state.newspaperBacklog[this.newspaper.fullName]
      return considered.filter(log => log.post.type === 'tweet')
    },
  },

  methods: {
    selectTweet(id) {
      this.selectedTweets[id] = !this.selectedTweets[id]
      this.$forceUpdate()
    }
  },
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
