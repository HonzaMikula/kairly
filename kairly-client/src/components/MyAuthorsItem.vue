<template>
  <my-authors--item style="border: 1px solid black">
    <h3>
      <router-link :to="author.url">{{ author.name }}</router-link>
    </h3>

    <AuthorSubscription
      :name="author.name" :subscription="author.subscription"
    />

  </my-authors--item>
</template>

<script>
import * as api from '@/api'

import AuthorSubscription from '@/components/widgets/AuthorSubscription'

export default {
  name: 'MyAuthorsItem',
  props: ['author'],

  components: {
    AuthorSubscription
  },

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
