<template>
  <author-widget-view>
    <header>
      <picture>
        <router-link :to="author.url">
          <img :src="author.picture" :alt="author.name"/>
        </router-link>
      </picture>
      <h3>
        <router-link :to="author.url">{{ author.name }}</router-link>
      </h3>
    </header>

    <p>{{ author.bio }}</p>

    <section>
      <AuthorSubscription
        :name="author.name" :subscription="author.subscription"
      />
    </section>
    

  </author-widget-view>
</template>

<script>
import * as api from '@/api'

import AuthorSubscription from '@/components/widgets/AuthorSubscription'

export default {
  name: 'AuthorWidget',
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
author-widget-view
  position: relative

  box-sizing: border-box
  display: block
  margin-bottom: $baseline / 2
  padding: $baseline / 4
  width: 576px

  background: #fff

  header 
    display: flex

    img
      border-radius: 100%
      height: $baseline * 1.5
      margin-right: $baseline / 2
      width: $baseline * 1.5  

    h3
      font-family: $ff-serif
      font-size: $fs-1

      a 
        color: #000

  p
    margin-bottom: $baseline / 2

    font-family: $ff-serif

  button
    +subscribe-button     

  section
    position: absolute
    right: $baseline / 4
    top: $baseline / 4

    font-family: $ff-sans !important

</style>
