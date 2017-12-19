<template>
  <post :post="post">
    <timeline-post--blog>
      <h2>{{ post.content.title }}</h2>
      <img :src="post.content.picture" :alt="post.content.title" />
      <p>{{ post.content.content }}</p>
    </timeline-post--blog>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-blog',
  props: ["post"],
  components: { post },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>