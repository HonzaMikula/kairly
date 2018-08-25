<template>
  <app-layout>
    <explore-view :class="$route.params.tab">
      <header>
        <nav>
          <ul>
            <li v-for="tab in tabs" :key="tab.slug">
              <nuxt-link :to="tab.slug ? '/explore/' + tab.slug : '/explore'" exact>{{ tab.name }}</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/explore/recent" exact>Most Recent</nuxt-link>
            </li>
          </ul>
        </nav>
        <h1>
          <portal-target name="explore-header" />
        </h1>
      </header>

      <nuxt-child/>
    </explore-view>
  </app-layout>
</template>

<script>
import TABS from '@/exploreTabs'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'Explore',

  components: {
    AppLayout
  },

  data() {
    return {
      tabs: TABS,
    }
  },

  async fetch({ store }) {
    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }
  }
}
</script>

<style lang="sass">
explore-view

  //- Header
  > header
    display: grid
    grid-template-columns: 100%
    grid-template-rows: auto $baseline*2
    grid-template-areas: "heading" "nav"

    height: 400px

    background: url('~/assets/homepage/hero.png') center center no-repeat
    background-size: cover

    @at-root .politics > header
      background-image: url('~/assets/explore/uspolitics.jpg')

    @at-root .sport > header
      background-image: url('~/assets/explore/olymp.jpg')

    @at-root .technology > header
      background-image: url('~/assets/explore/bitcoin.jpg')

    @at-root .lifecd  > header
      background-image: url('~/assets/explore/life.jpg')

    @media (max-width: $mobile)
      height: 200px

      grid-template-rows: auto min-content

    nav
      grid-area: nav

      backdrop-filter: blur(5px)
      background: rgba(0, 0, 0, 0.05)

      ul
        display: table
        margin: 0 auto

      li
        display: inline-block

      a
        display: block
        padding: 0 $baseline/2

        color: #fff

        line-height: $baseline * 2

        &:hover,
        &:focus,
        &.is-active
          background: rgba(0, 0, 0, 0.3)



    h1
      grid-area: heading
      align-self: center
      justify-self: center

      color: #fff

      font-size: 60px
      font-family: $ff-serif
      text-shadow: 0 0 10px #000

      @media (max-width: $mobile)
        font-size: $fs-4


  //- Sections
  main
    display: grid
    max-width: 970px
    margin: $baseline auto
    grid-column-gap: $baseline
    grid-row-gap: $baseline
    grid-template-columns: 50% 50%
    grid-template-rows: auto auto
    grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-0 explore-1" "explore-2 explore-3"

    @media (max-width: $mobile)
      padding: 0 $baseline/4
      grid-template-columns: 100%
      grid-template-areas: "explore-top-newspapers" "explore-0" "explore-1" "explore-2" "explore-3"


  @at-root .recent > main
    grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-recent explore-recent"

explore--top-newspapers
  grid-area: explore-top-newspapers

  > h2
    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 2

  //-- wrapper
  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2

    @media (max-width: $mobile)
      grid-template-columns: 1fr 1fr

      newspaper-widget-view:last-of-type
        display: none

section
  > h2
    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 2

  &.explore-0
    grid-area: explore-0

  &.explore-1
    grid-area: explore-1

  &.explore-2
    grid-area: explore-2

  &.explore-3
    grid-area: explore-3

  &.explore-recent
    grid-area: explore-recent
</style>
