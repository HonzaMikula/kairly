<template>
  <tweet-attachment-gif-view>
    <video v-for="item in items" :key="item.src" :poster="item.src" :width="item.sizes.small.w" muted loop autoplay>
      <source
        :src="item.video_info.variants[0].url"
        :type="item.video_info.variants[0].content_type" />
    </video>
  </tweet-attachment-gif-view>
</template>

<script>
export default {
  name: 'tweet-attachment-gif',

  props: ["items"],
}
</script>

<style lang="sass">
tweet-attachment-gif-view
  display: block
  margin-top: $baseline / 2
  margin-bottom: -($baseline/2)

  video
    display: block
    width: 100%

</style>
