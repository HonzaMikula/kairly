<template>
  <newspaper-widget-view>
    <picture>
      <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">
        <img v-if="newspaper.picture" :src="newspaper.picture" :alt="newspaper.title" />
        <div v-else class="image-placeholder"></div>
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

    <newspaper-widget--subscribe v-if="loggedIn">
      <newspaper-subscription :newspaper="newspaper" />

      <p>
        #{{ newspaper.issues }}
        •
        {{ newspaper.likes }} {{ $t('subscribers') }}
      </p>
    </newspaper-widget--subscribe>

  </newspaper-widget-view>
</template>

<script>

import { mapState } from 'vuex'

import { getPeriodicityLabel } from '@/utils/period'
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'

export default {
  name: 'NewspaperWidget',

  props: {
    newspaper: Object
  },

  components: {
    NewspaperSubscription
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    periodicity() {
      return getPeriodicityLabel(this.newspaper.periodicity)
    }
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

    .image-placeholder
      height: 100%
      background-image: radial-gradient(#fafafa, #aaa)


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

    font-size: $fs--1
    font-weight: 600
    line-height: $baseline * 0.8

  //- description
  > p
    flex: 1
    order: 5

    color: #777

    font-size: $fs--1
    line-height: $baseline * 0.8

//- Author + Periodicity
newspaper-widget--author
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

  button
    height: $baseline !important
    line-height: $baseline !important


  //- info
  p
    font-size: $fs--1

    @media (max-width: $mobile)
      display: none
</style>
