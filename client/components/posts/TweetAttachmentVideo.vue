<template>
  <div class="tweet-attachment-video-view">
    <video :poster="item.src" :width="item.sizes.small.w" controls>
      <source
        :src="item.video_info.variants[0].url"
        :type="item.video_info.variants[0].content_type" />
    </video>
  </div>
</template>

<script>
export default {
  name: 'tweet-attachment-video',

  props: ["item"],
}
</script>

<style lang="sass">
.tweet-attachment-video-view
  display: block
  margin-top: $baseline / 2

  video
    display: block
    width: 100%

</style>
