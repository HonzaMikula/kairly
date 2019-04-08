<template>
  <PostBase :post="post">
    <div>
      <h2>
        <a :href="post.source" target="_blank">{{ post.content.title }}</a>
      </h2>
      <div v-if="post.content.attachments && post.content.attachments.image">
        <img height="200" :src="post.content.attachments.image"/>
      </div>
      <div v-html="post.content.perex"></div>
    </div>
    <template slot="controls"><slot name="controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'post-link',

  props: ["post", "isSubscribed"],

  components: { PostBase }
}
</script>

<style lang="sass">
