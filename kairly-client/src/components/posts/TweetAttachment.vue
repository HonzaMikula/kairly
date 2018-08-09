<template>
  <tweet-attachment-view>
    <a v-if="baseType === 'url'"
       class="external-url"
       :href="item.href">
      <h4>{{ item.title }}</h4>
      <p class="external-url--netloc" :href="item.href">{{ item.host }}</p>
    </a>

    <img v-else-if="item.type == 'media.photo'" :src="`${item.src}:small`" :width="item.sizes.small.w" height="item.sizes.small.h" />
    <video v-else-if="item.type == 'media.animated_gif'" :poster="item.src" :width="item.sizes.small.w" loop autoPlay>
      <source
        :src="item.video_info.variants[0].url"
        :type="item.video_info.variants[0].content_type" />
    </video>


    <div v-else-if="item.type == 'quoted_status.unavailable'" class="quoted-status">
      <em>This Tweet is unavailable.</em>
    </div>
    <div v-else-if="baseType === 'quoted_status'" class="quoted-status">
      <div>
        <a class="quoted-status--username" :href="item.user.url">{{ item.user.name }}</a>
        <a class="quoted-status--userid" :href="item.user.url">@{{ item.user.screen_name }}</a>
      </div>
      <div v-html="item.content"></div>
      <tweet-attachment v-for="a in item.attachments" :item="a" :key="a.id || a.href"/>
    </div>
  </tweet-attachment-view>
</template>

<script>

import post from './post';

export default {
  name: 'tweet-attachment',

  props: ["item"],

  computed: {
    baseType() {
      return this.item.type.split('.')[0]
    }
  }
}
</script>

<style lang="sass">
tweet-attachment-view
  display: block
  margin-top: $baseline / 4
  margin-bottom: -($baseline/2)

  font-size: $fs--1

  > a
    display: block
    padding: $baseline/4

    background: #fafafa

    &:hover,
    &:focus
      background: #eee

    h4
      color: #000

  .external-url--netloc
    color: #999

  .quoted-status
    // !!! be aware that external url can be probably also nested inside quoted-status
    font-size: $fs--1 !important
    line-height: 1.2

  .quoted-status--username
    font-weight: 600


</style>
