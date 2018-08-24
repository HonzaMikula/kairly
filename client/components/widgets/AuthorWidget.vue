<template>
  <author-widget-view>
    <header>
      <picture>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          <img :src="author.picture" :alt="author.name"/>
        </nuxt-link>
      </picture>
      <h3>
        <nuxt-link :to="{name: 'author', params: {author: author.id}}">
          {{ author.name }}
        </nuxt-link>
      </h3>

      <section>
        <AuthorSubscription
          v-if="subscription"
          :subscription="subscription" :author="author"
        />

        <button
          v-else
          @click="$refs.followWidget.openSubscribeWidget()">
          Subscribe author
        </button>

        <follow-author
          ref="followWidget"
          :author="author"
          :onSelect="follow"
        />

      </section>
    </header>

    <p>{{ author.bio }}</p>
  </author-widget-view>
</template>

<script>
import * as api from '@/api'

import AuthorSubscription from '@/components/widgets/AuthorSubscription'
import FollowAuthor from '@/components/widgets/FollowAuthor'

export default {
  name: 'AuthorWidget',

  props: {
    author: Object
  },

  components: {
    FollowAuthor,
    AuthorSubscription
  },

  computed: {
    subscription() {
      return this.$store.state.subscriptions.authors[this.author.id]
    }
  },

  methods: {
    follow(periodicity) {
      this.$store.dispatch('subscribeAuthor', {
        authorId: this.author.id,
        periodicity
      })
    }
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

  > header
    display: grid
    grid-column-gap: $baseline / 4
    grid-template-columns: $baseline*1.25 1fr auto
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

    //- subscription information
    author-subscription-view
      font-family: $ff-sans !important
      text-align: right

    //- subscribe button
    section
      position: relative

      grid-area: author-widget-subscription
      justify-self: end

      font-size: $fs--2

      button
        +subscribe-button

        height: $baseline
        padding: 0 $baseline/2

        font-family: $ff-sans
        font-size: $fs--2
        line-height: $baseline

  //- bio
  p
    margin-bottom: $baseline / 2

    color: #777

    font-size: $fs--2
    line-height: $baseline * 0.8

</style>
