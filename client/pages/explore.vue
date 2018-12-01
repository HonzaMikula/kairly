<template>
  <app-layout>
    <explore-view :class="$route.name === 'explore-recent' ? 'recent' : $route.params.tab">
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
    background: #eee

    nav
      margin: 0 auto
      max-width: 900px

      ul
        @media (max-width: $mobile)
          display: block

          white-space: nowrap
          overflow-x: auto

      li
        display: inline-block

      a
        display: block
        padding: 0 $baseline/2

        color: #555

        font-size: $fs-1
        line-height: $baseline * 2

        &:hover,
        &:focus,
        &.nuxt-link-active
          background: #ddd


  //- Sections
  main
    display: grid
    max-width: 900px
    margin: $baseline/2 auto
    grid-column-gap: $baseline
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr
    grid-template-rows: auto auto
    grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-0 explore-1" "explore-2 explore-3"

    @media (max-width: $mobile)
      padding: 0 $baseline/4
      grid-template-columns: 100%
      grid-template-areas: "explore-top-newspapers" "explore-0" "explore-1" "explore-2" "explore-3"


  @at-root .recent > main
    grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-recent explore-recent"

    @media (max-width: $mobile)
      grid-template-areas: "explore-top-newspapers" "explore-recent"

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
      grid-column-gap: $baseline / 4
      overflow-x: auto

      newspaper-widget-view,
      issue-widget-view
        min-width: 200px

</style>
