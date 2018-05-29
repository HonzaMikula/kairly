<template>
  <my-authors--item>

  </my-authors--item>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'MyAuthorsItem',
  props: ['author'],

  methods: {
    // subscribe(ev) {
    //   const value = !this.edition.isSubscribed
    //   this.$store.dispatch('subscribe', {
    //     edition: this.edition,
    //     value
    //   })
    //   ev.target.blur()
    // }
  }
}
</script>

<style lang="sass">
</style>
