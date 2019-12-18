<template>
  <div class="tweet-attachment-link-view">
    <a :href="item.href">
      <h4>{{ item.title }}</h4>
      <p>{{ item.host }}</p>
    </a>
  </div>
</template>

<script>
export default {
  name: 'tweet-attachment-link',

  props: ["item"]
}
</script>

<style lang="sass">
.tweet-attachment-link-view
  display: block
  margin-top: $baseline / 2

  box-shadow: 3px 3px 3px #eee

  font-size: $fs-0

  a
    display: block
    padding: $baseline/4

    background: #fafafa

    &:hover,
    &:focus
      background: #eee

    h4
      color: #000

    p
      color: #999

      font-size: $fs--1


</style>
