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

      <AuthorSubscription
        :name="author.name" :subscription="author.subscription"
      />
    </header>

    <p>{{ author.bio }}</p>
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
  max-width: 576px

  background: #fff

  header 
    display: grid
    grid-column-gap: $baseline / 4
    grid-template-columns: $baseline*1.25 auto auto
    grid-template-rows: $baseline * 1.25
    grid-template-areas: "author-widget-image author-widget-name author-widget-subscription"
    align-items: center
    margin-bottom: $baseline / 4

    //- picture
    img
      grid-area: author-widget-image

      display: block
      border-radius: 100%
      height: $baseline * 1.25
      margin-right: $baseline / 2
      width: $baseline * 1.25  

    //- name
    h3
      grid-area: author-widget-name

      font-weight: 600

      a 
        color: #000

        text-decoration: none

    //- subscription information
    author-subscription-view
      grid-area: author-widget-subscription

      font-family: $ff-sans !important    
      text-align: right
  
  //- bio
  p
    margin-bottom: $baseline / 2

    color: #777

    font-size: $fs--2
    line-height: $baseline * 0.8

</style>
