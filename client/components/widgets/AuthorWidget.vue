<template>
  <div class="author-widget-view">
    <header>
      <picture>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          <AuthorPicture :author="author" />
        </nuxt-link>
      </picture>
      <h3>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          {{ author.name }}
        </nuxt-link>
      </h3>

      <section>
        <AuthorSubscriptionButton :author="author" />
      </section>
    </header>

    <p>{{ author.bio }}</p>
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorSubscriptionButton from '@/components/widgets/AuthorSubscriptionButton'

export default {
  name: 'AuthorWidget',

  props: {
    author: Object
  },

  components: {
    AuthorPicture,
    AuthorSubscriptionButton
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

//- Author Widget View -//
.author-widget-view
  position: relative

  box-sizing: border-box
  display: block
  margin-bottom: $baseline / 2
  padding: $baseline / 4
  max-width: 576px

  background: #fff

  > header
    display: grid
    grid-column-gap: $baseline / 4
    grid-template-columns: $baseline*1.25 1fr auto
    grid-template-rows: minmax($baseline * 1.25, auto)
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
      line-height: 1.42
      word-wrap: break-word
      hyphens: auto

      a
        color: #000

    //- subscription information
    author-subscription-view
      font-family: $ff-sans !important
      text-align: right


    //- subscribe button
    section
      position: relative

      grid-area: author-widget-subscription
      min-width: 120px

      font-size: $fs--1
      text-align: right

  //- bio
  > p
    margin-bottom: $baseline / 2

    color: #777

    font-size: $fs--1
    line-height: $baseline * 0.8

</style>
