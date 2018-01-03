<template>
  <post :post="post" v-on:readlater="readLaterMessage(el)">
    <timeline-post--picture>
      <figure>
        <img :src="post.content.picture" :alt="post.content.title" />
        
        <figcaption>{{ post.content.title }}</figcaption>
      </figure>
    </timeline-post--picture>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-picture',
  props: ["post"],
  components: { post },
  methods: {
    readLaterMessage: function() {
      this.$emit('readlater')
    }
  }
}
</script>