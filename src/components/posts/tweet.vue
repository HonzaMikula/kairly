<template>
  <post :post="post" v-on:readlater="readLaterMessage()">
    <timeline-post--tweet>
      <p v-html="post.content"></p>
    </timeline-post--tweet>
  </post>
</template>

<script>

import post from './post';

export default {
  name: 'post-tweet',
  props: ["post"],
  components: { post },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>