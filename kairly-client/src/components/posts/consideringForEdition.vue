<template>
  <post :post="post">
    <timeline-post--tweet>
      <p v-html="post.content"></p>
    </timeline-post--tweet>
  </post>
</template>

<script>

import post from './post';

export default {
  name: 'consideringForEdition',
  props: ["post"],
  components: { post },
}
</script>
