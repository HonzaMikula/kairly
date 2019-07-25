<template>
  <div class="tweet-attachment-link-view">
    <div v-for="item in items" :key="item.href">
      <a :href="item.href">
        <h4>{{ item.title }}</h4>
        <p>{{ item.host }}</p>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'tweet-attachment-link',

  props: ["items"]
}
</script>

<style lang="sass">
.tweet-attachment-link-view
  display: block
  margin-top: $baseline / 2

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
