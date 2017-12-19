<template>
  <post-detail role="article">

  <post-detail--back-button 
    v-tooltip.right="'Back to Browsing Editions'"
    v-on:click="$router.push('/')">
  </post-detail--back-button>

    <div>
      <post-detail--header>
        <img :src="postDetail.author.picture" :alt="postDetail.author.name"/>
        <author-name>{{postDetail.author.name}}</author-name>
        <author-follow>Follow</author-follow>
        <author-description>{{postDetail.author.description}}</author-description>

        <button-read-later></button-read-later>
      </post-detail--header>
      
      <post-detail--title>
        <h1>{{postDetail.title}}</h1>
      </post-detail--title>

      <post-detail--content v-html="postDetail.content"></post-detail--content>

      <post-detail--footer>
        <button-icon class="favorite" v-tooltip.top="'Favorite'"></button-icon>
        <button-icon class="share" v-tooltip.top="'Share'"></button-icon>
        <button-icon class="edition" v-tooltip.top="'Consider for Edition'"></button-icon>
      </post-detail--footer>


    </div>
  </post-detail>
</template>

<script>
import postDetail from '@/data/postDetail.json'

export default {
  name: 'hello',
  data: function() {
    return {
      postDetail
    }
  }
}
</script>
