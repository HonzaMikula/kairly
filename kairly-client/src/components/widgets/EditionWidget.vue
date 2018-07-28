<template>
  <edition-widget-view>
    <picture>
      <router-link :to="{name: 'edition', params: {author: edition.editor.id, edition: edition.name}}">
        <img :src="edition.picture" :alt="edition.title" />
      </router-link>
    </picture>

    <h2>
      <router-link :to="{name: 'edition', params: {author: edition.editor.id, edition: edition.name}}">{{ edition.title }}</router-link>
    </h2>

    <p>{{ edition.description }}</p>

    <edition-widget--author>
      <img :src="edition.editor.picture" :alt="edition.editor.name"/>
      <router-link :to="{name: 'author', params: {author: edition.editor.id}}">{{ edition.editor.name }}</router-link>
    </edition-widget--author>

    <edition-widget--subscribe>
      <button
        v-if="isSubscribed"
        class="is-subscribed"
        @click="unsubscribe($event)">
        <span class="default">Subscribed</span>
        <span class="on-hover">Unsubscribe</span>
      </button>

      <button
        v-else
        class="to-subscribe"
        @click="subscribe($event)">
        Subscribe
      </button>

      <p>
        {{ edition.periodicity.frequency }} {{ edition.periodicity.time }} {{ edition.periodicity.dow }}
        •
        {{ edition.likes }} subscribers
        •
        #{{ edition.issues }}
      </p>
    </edition-widget--subscribe>

  </edition-widget-view>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'EditionWidget',

  props: {
    edition: Object
  },

  computed: {
    isSubscribed() {
      return this.edition.fullName in this.$store.state.subscriptions.editions
    }
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', this.edition.fullName)
      document.activeElement.blur()
    },

    unsubscribe(ev) {
      this.$store.dispatch('unsubscribe', this.edition.fullName)
      document.activeElement.blur()
    },
  }
}
</script>

<style lang="sass">
edition-widget-view
  position: relative

  display: flex
  flex-direction: column
  flex: 1 0 270px
  padding: 0 $baseline / 4
  border-radius: $baseline / 4
  overflow: hidden

  background: #fff
  border: 1px solid #eee

  text-align: left


  //- header picture
  picture
    order: 1
    display: block
    margin: 0 (-$baseline)/4 0 (-$baseline)/4
    height: 120px

    @media (max-width: $mobile)
      height: 80px

    img
      height: 100%
      width: 100%
      object-fit: cover

  //- title
  > h2
    order: 3
    font-weight: 600

    a
      color: #000

  //- description
  > p
    flex: 1
    order: 4

    color: #777

    font-size: $fs--2
    line-height: $baseline * 0.8

//- Author + Periodicity
edition-widget--author
  font-size: $fs--1
  order: 2
  margin: $baseline/2 0

  @media (max-width: $mobile)
    margin: $baseline/4 0

  img
    border-radius: 100%
    float: left
    height: $baseline
    margin-right: $baseline / 4
    width: $baseline

    object-fit: cover

  a
    color: #000


//- Subscribe Edition
edition-widget--subscribe
  display: block
  padding: $baseline / 2 0 0 0
  order: 4

  text-align: center

  @media (max-width: $mobile)
    padding-bottom: $baseline / 4

  //- when edition is subscribed
  button.is-subscribed
    +subscribed-button

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when edition is ready to be subsribed
  button.to-subscribe
    +subscribe-button

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

  //- info
  p
    font-size: $fs--2

    @media (max-width: $mobile)
      display: none
</style>
