<template>
  <div class="tweet-attachment-quote-view">
    <h4><a :href="item.user.url">{{ item.user.name }}</a></h4>
    <p v-html="item.content" />
  </div>
</template>

<script>
export default {
  name: 'TweetAttachmentQuote',

  props: {
    item: { type: Object, required: true }
  }
}
</script>

<style lang="sass">
.tweet-attachment-quote-view
  display: block
  margin-top: $baseline / 4
  padding: $baseline/4

  background: #fafafa
  box-shadow: 2px 2px 2px #eee, -2px -2px 4px #fff

  font-size: $fs-0

  a
    color: $c-base

  h4
    font-family: $ff-sans
    font-size: $fs--1
    font-weight: 600

    a
      color: #555

  p
    font-size: $fs--1
    line-height: 1.58

</style>
