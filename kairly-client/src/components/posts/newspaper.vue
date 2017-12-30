<template>
  <post :post="post" v-on:readlater="readLaterMessage()">
    <timeline-post--newspaper>
      <h2>{{ post.content.title }}</h2>
      <timeline-post--newspaper--content v-html="this.postContent"></timeline-post--newspaper--content>
    </timeline-post--newspaper>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-newspaper',
  props: ["post"],
  data: function () {
    return {
      postContent: ''
    }
  },
  components: { post },
  created: function() {
    var content = this.post.content.content;
    if (this.post.timeRead) {
      var content = this.post.content.content + '<timeline-post--continue-reading><a href="/post">Continue reading</a> ('+ this.post.timeRead +')</timeline-post--continue-reading>';
    }
    this.postContent = content;
  },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>