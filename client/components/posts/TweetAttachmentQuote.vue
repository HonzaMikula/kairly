<template>
  <div class="tweet-attachment-quote-view">
    <div v-for="item in items" :key="item.user.url">
      <h4><a :href="item.user.url">{{ item.user.name }}</a></h4>
      <p v-html="item.content"></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'tweet-attachment-quote',

  props: ["items"]
}
</script>

<style lang="sass">
.tweet-attachment-quote-view
  display: block
  margin-top: $baseline / 4
  padding: $baseline/4

  background: #fafafa

  font-size: $fs-0

  a
    color: $c-base

  h4
    margin-bottom: $baseline / 4

  p
    line-height: 1.58




</style>
