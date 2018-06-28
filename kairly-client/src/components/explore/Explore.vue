<template>
  <app-layout>
    <explore-view :class="tab.slug">
      <header>
        <nav>
          <ul>
            <li v-for="tab in tabs" :key="tab.slug"><router-link :to="tab.slug ? '/explore/' + tab.slug : '/explore'" exact>{{ tab.name }}</router-link></li>
          </ul>
        </nav>
        <h1>{{ tab.name }}</h1>
      </header>

      <explore-recent v-if="tab.slug === 'recent'" />
      <explore-content v-else :tab="tab" />
    </explore-view>
  </app-layout>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'
import TABS from './exploreTabs'

import AppLayout from '@/components/layout/AppLayout'
import ExploreContent from '@/components/explore/ExploreContent'
import ExploreRecent from '@/components/explore/ExploreRecent'


export default {
  name: 'Explore',

  metaInfo() {
      return {
        title: this.tab ? `Explore - ${this.tab.name}` : 'Explore',
      }
  },

  components: {
    AppLayout,
    ExploreContent,
    ExploreRecent
  },

  data() {
    return {
      tabs: TABS,
    }
  },

  computed: {
    tab() {
      const slug = this.$route.params.tab
      return TABS.find(t => t.slug === slug)
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

    background: url(../../assets/homepage/hero.png) center center no-repeat
    background-size: cover

    @at-root .politics > header
      background-image: url(http://kairly.com/media/editions/uspolitics.jpg)

    @at-root .sport > header
      background-image: url(http://kairly.com/media/editions/olymp.jpg)

    @at-root .technology > header
      background-image: url(http://kairly.com/media/editions/bitcoin.jpg)

    @at-root .lifestyle > header
      background-image: url(http://www.celiaxmoni.cz/wp-content/uploads/2018/05/222C8379-5FE4-42C4-91B9-4C441AC7AC6F.jpeg)

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


  //- Sections
  main
    display: grid
    max-width: 970px
    margin: $baseline auto
    grid-column-gap: $baseline
    grid-row-gap: $baseline
    grid-template-columns: 50% 50%
    grid-template-rows: auto auto
    grid-template-areas: "explore-top-editions explore-top-editions" "explore-0 explore-1" "explore-2 explore-3"

  @at-root .recent > main
    grid-template-areas: "explore-top-editions explore-top-editions" "explore-recent explore-recent"

explore--top-editions
  grid-area: explore-top-editions

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
