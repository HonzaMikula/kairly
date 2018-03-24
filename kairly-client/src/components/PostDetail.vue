<template>
  <post-detail role="article">
    <post-detail--back-button
      v-tooltip.right="'Back to Browsing Editions'"
      v-on:click="$router.go(-1)">
    </post-detail--back-button>

    <post-detail--read-later
      v-tooltip.right="'Read Later'">
    </post-detail--read-later>

    <div v-if="post">
      <post-detail--header>
        <router-link :to="post.author.url">
          <img :src="post.author.picture" :alt="post.author.name"/>
          {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </router-link>

        <button-icon class="read-later" v-tooltip.top="'Read Later'"></button-icon>
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
        <button-icon class="recommend">Recommend</button-icon>
        <button-icon class="share">Share</button-icon>
        <button-icon class="consider-for-edition">Consider for Edition</button-icon>
      </post-detail--footer>

      <post-detail--author>
        <picture>
          <router-link :to="post.author.url">
            <img :src="post.author.picture" :alt="post.author.name"/>
          </router-link>
        </picture>
        
        <h3>
          <router-link :to="post.author.url">
            {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
          </router-link>
        </h3>

        <p>{{post.author.bio}}</p>
      </post-detail--author>

    </div>
  </post-detail>
</template>

<script>
import request from 'superagent'
import * as api from '@/api'

export default {
  name: 'PostDetailPage', // can't use PostDetail because post-detail is already used
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
