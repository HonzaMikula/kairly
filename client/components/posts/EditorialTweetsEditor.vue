<template>
  <div class="editorial-post-editor">
    <article role="article" class="post newspaper editorial">
      <header>
        <picture>
          <a href="/janmikula" class="">
            <img src="https://cdn.kairly.com/media/users/janmikula.jpg" alt="Dojnice">
          </a>
        </picture>
        <h3>
          <a href="/janmikula" class="">Jan Mikula, editor</a>
        </h3>
      </header>

      <div v-if="tweets.length">
        <PostTweet v-for="tweet in tweets" :key="tweet.id" :post="tweet">
          <template slot="controls">
            <a
              href="#"
              @click.prevent="$emit('removeTweet', tweet)"
            >Remove</a>
          </template>
        </PostTweet>
      </div>
      <div v-else>
          Add tweets here.
      </div>
    </article>
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

</style>
