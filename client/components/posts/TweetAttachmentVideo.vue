<template>
  <div class="tweet-attachment-video-view">
    <video
      :poster="item.src"
      :preload="none"
      :width="dim[0]"
      :height="dim[1]"
      :duration="item.video_info.duration_millis / 1000"
      controls
      playsinline
    >
      <!--source
        v-for="(source, idx) in item.video_info.variants"
        :key="idx"
        :src="source.url"
        :type="source.content_type"
      /-->
    </video>
  </div>
</template>

<script>
const MAX_SIZE = 576

export default {
  name: 'tweet-attachment-video',

  props: ["item"],

  computed: {
    dim() {
      const ar = this.item.video_info.aspect_ratio
      const dim1 = [MAX_SIZE, parseInt(MAX_SIZE / ar[0] * ar[1])]
      const dim2 = [parseInt(MAX_SIZE / ar[1] * ar[0]), MAX_SIZE]
      return dim1[1] > MAX_SIZE ? dim2 : dim1
    }
  }
}
</script>

<style lang="sass">
.tweet-attachment-video-view
  display: block
  margin-top: $baseline / 2

  video
    display: block
    max-width: 100%

</style>
