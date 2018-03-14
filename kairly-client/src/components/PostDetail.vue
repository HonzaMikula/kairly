<template>
  <post-detail role="article">

  <post-detail--back-button
    v-tooltip.right="'Back to Browsing Editions'"
    v-on:click="$router.go(-1)">
  </post-detail--back-button>

    <div v-if="post">
      <post-detail--header>
        <img :src="post.author.picture" :alt="post.author.name"/>
        <author-name>{{post.author.name}}</author-name>
        <author-follow><router-link :to="post.author.url">Author detail</router-link></author-follow>
        <author-description>{{post.author.bio}}</author-description>

        <button-read-later></button-read-later>
      </post-detail--header>

      <post-detail--title>
        <h1>{{post.content.title}}</h1>
      </post-detail--title>

      <post-detail--content v-html="post.content.perex"></post-detail--content>

      <post-detail--continue-reading id="continue">
        continue reading
      </post-detail--continue-reading>

      <post-detail--content v-html="post.content.content"></post-detail--content>

      <post-detail--footer>
        <button-icon class="favorite" v-tooltip.top="'Favorite'"></button-icon>
        <button-icon class="share" v-tooltip.top="'Share'"></button-icon>
        <button-icon class="edition" v-tooltip.top="'Consider for Edition'"></button-icon>
      </post-detail--footer>

    </div>
  </post-detail>
</template>

<script>
import request from 'superagent'
import * as api from '@/api'

export default {
  name: 'PostDetail',
  data: function() {
    return {
      post: null
    }
  },
  created: function () {
    api.getPost(this.$route.params.postId).then(post => this.post = post)
  },
  updated: function() {
    // TODO dangerous if more component properties exists and updated called more
    // then once
    if (this.$route.hash) {
      const anchor = document.querySelector(this.$route.hash)
      if (anchor) {
        anchor.scrollIntoView(true)
      }
    }
  }
}
</script>
