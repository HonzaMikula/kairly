<template>
  <post :post="post">
    <timeline-post--article>
      <h2>{{ post.content.title }}</h2>
      <img :src="post.content.picture" :alt="post.content.title" />
      <p>{{ post.content.perex }}</p>
    </timeline-post--article>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-article',
  props: ["post"],
  components: { post },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>