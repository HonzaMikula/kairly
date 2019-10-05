<template>
  <div class="author-popup-view">
    <header>
      <picture>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          <img
            v-if="author.picture"
            :src="author.picture"
            :alt="author.name"
          />
          <img
            v-else
            src="~assets/user.png"
            :alt="author.name"
          />
        </nuxt-link>
      </picture>
      <h3>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          {{ author.name }}
        </nuxt-link>
      </h3>
      <p v-if="author.medium">{{ author.medium }}</p>
    </header>

    <p>{{ author.bio }}</p>

    <section>
      <AuthorSubscription :author="author" />
    </section>
  </div>
</template>

<script>
import AuthorSubscription from '@/components/widgets/AuthorSubscription'

export default {
  name: 'AuthorPopup',

  props: {
    author: Object
  },

  components: {
    AuthorSubscription
  },

  computed: {
    subscription() {
      return this.$store.getters.getAuthorSubscription(this.author)
    },
    canceled() { return this.subscription && this.subscription.state == 'canceled'}
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Author Popup View -//
.author-popup-view
  position: relative

  box-sizing: border-box
  display: block
  padding: $baseline / 4
  width: 276px

  background: #fff

  > header
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-columns: $baseline*2 auto
    grid-template-rows: minmax($baseline * 1.25, auto) auto
    grid-template-areas: "author-widget-image author-widget-name" "author-widget-image author-widget-medium"
    align-items: center
    margin-bottom: $baseline / 4

    //- picture
    picture
      grid-area: author-widget-image

    img
      display: block
      border-radius: 100%
      height: $baseline * 2
      width: $baseline * 2

    //- name
    h3
      grid-area: author-widget-name

      font-weight: 600
      font-size: $fs-1
      line-height: $baseline * 1.25
      word-wrap: break-word
      hyphens: auto

      a
        color: #000

    p
      grid-area: author-widget-medium

      font-size: $fs--1
      line-height: $baseline * 0.75
      
  //- bio
  > p
    margin-bottom: $baseline / 2

    color: #777

    font-size: $fs--1
    line-height: $baseline * 0.8

  //- subscribe button
  > section
    position: relative

    font-size: $fs--1
    text-align: center

    //- subscription information
    author-subscription-view
      font-family: $ff-sans !important
      text-align: right

</style>
