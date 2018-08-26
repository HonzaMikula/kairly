<template>
  <newspaper-widget-view>
    <picture>
      <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">
        <img :src="newspaper.picture" :alt="newspaper.title" />
      </nuxt-link>
    </picture>

    <h2>
      <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">{{ newspaper.title }}</nuxt-link>
    </h2>

    <time>{{ periodicity }}</time>

    <p>
      {{ newspaper.description }}
    </p>

    <newspaper-widget--author>
      <img :src="newspaper.editor.picture" :alt="newspaper.editor.name"/>
      <nuxt-link :to="{name: 'author', params: {author: newspaper.editor.id}}">{{ newspaper.editor.name }}</nuxt-link>
    </newspaper-widget--author>

    <newspaper-widget--subscribe>
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
        #{{ newspaper.issues }}
        •
        {{ newspaper.likes }} subscribers
      </p>
    </newspaper-widget--subscribe>

  </newspaper-widget-view>
</template>

<script>


export default {
  name: 'NewspaperWidget',

  props: {
    newspaper: Object
  },

  data() {
    return {
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    isSubscribed() {
      return this.$store.getters.getNewspaperSubscription(this.newspaper)
    },

    periodicity() {
      if (this.newspaper.periodicity.frequency == '3x_per_day') {
        return 'Daily at 6:00, 12:00 and 18:00'
      }
      else if (this.newspaper.periodicity.frequency == 'daily') {
        return `Daily at ${this.newspaper.periodicity.time}`
      }
      else {
        return `Every ${this.DAYS[this.newspaper.periodicity.dow -1]} at ${this.newspaper.periodicity.time}`
      }
    }
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribeNewspaper', this.newspaper.fullName)
      document.activeElement.blur()
    },

    unsubscribe(ev) {
      this.$store.dispatch('unsubscribeNewspaper', this.newspaper.fullName)
      document.activeElement.blur()
    },
  }
}
</script>

<style lang="sass">
newspaper-widget-view
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

  //- periodicity
  > time
    order: 4
    margin-bottom: $baseline / 4

    color: #777

    font-size: $fs--2
    font-weight: 600
    line-height: $baseline * 0.8

  //- description
  > p
    flex: 1
    order: 5

    color: #777

    font-size: $fs--2
    line-height: $baseline * 0.8

//- Author + Periodicity
newspaper-widget--author
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


//- Subscribe Newspaper
newspaper-widget--subscribe
  display: block
  padding: $baseline / 2 0 0 0
  order: 6

  text-align: center

  @media (max-width: $mobile)
    padding-bottom: $baseline / 4

  //- when newspaper is subscribed
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

  //- when newspaper is ready to be subsribed
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
