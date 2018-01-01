<template>
  <post-detail role="article">

  <post-detail--back-button
    v-tooltip.right="'Back to Browsing Editions'"
    v-on:click="$router.push('/')">
  </post-detail--back-button>

    <div>
      <post-detail--header>
        <img :src="post.author.picture" :alt="post.author.name"/>
        <author-name>{{post.author.name}}</author-name>
        <author-follow>Follow</author-follow>
        <author-description>{{post.author.bio}}</author-description>

        <button-read-later></button-read-later>
      </post-detail--header>

      <post-detail--title>
        <h1>{{post.content.title}}</h1>
      </post-detail--title>

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

export default {
  name: 'hello',
  data: function() {
    return {
      post: null
    }
  },
  created: function () {
    const postId = this.$route.params.postId;
    request
      .get(process.env.BACKEND_BASE + '/api/post/' + postId)
      .then(res => {
        this.post = res.body.post
      })
  }

}
</script>
