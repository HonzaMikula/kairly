<template>
  <div class="tweet-attachment-gif-view">
    <video :poster="item.src" :width="item.sizes.small.w" muted loop autoplay>
      <source
        :src="item.video_info.variants[0].url"
        :type="item.video_info.variants[0].content_type"
      >
    </video>
  </div>
</template>

<script>
export default {
  name: 'TweetAttachmentGif',

  props: {
    item: { type: Object, required: true }
  }
}
</script>

<style lang="sass">
.tweet-attachment-gif-view
  display: block
  margin-top: $baseline / 2

  video
    display: block
    width: 100%

</style>
