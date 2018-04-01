<template>
  <post :post="post">
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
  props: ["post", "isSubscribed"],
  components: { post }
}
</script>
