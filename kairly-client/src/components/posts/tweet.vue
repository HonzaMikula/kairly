<template>
  <post :post="post" v-on:readlater="readLaterMessage()">
    <timeline-post--tweet>
      <p v-html="post.content.content"></p>
      <img :src="post.content.picture" v-if="post.content.picture" />
    </timeline-post--tweet>
  </post>
</template>

<script>

import post from './post';

export default {
  name: 'post-tweet',
  props: ["post", "isSubscribed"],
  components: { post },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>
