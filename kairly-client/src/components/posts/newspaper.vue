<template>
  <post :post="post" v-on:readlater="readLaterMessage()">
    <timeline-post--newspaper>
      <h2>{{ post.content.title }}</h2>
      <timeline-post--newspaper--content >
        <div v-html="post.content.content"></div>
        <timeline-post--continue-reading v-if="post.timeRead">
          <a href="/post">Continue reading</a> ({{ post.timeRead }})
        </timeline-post--continue-reading>
      </timeline-post--newspaper--content>
    </timeline-post--newspaper>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-newspaper',
  props: ["post"],
  components: { post },
  created: function() {
  },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>
