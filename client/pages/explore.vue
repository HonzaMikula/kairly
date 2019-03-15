<template>
  <AppLayout :name="$t('Explore')">
    <explore-view :class="$route.name === 'explore-recent' ? 'recent' : $route.params.tab">
      <header>
        <nav>
          <ul>
            <li v-for="tab in tabs" :key="tab.slug">
              <nuxt-link :to="tab.slug ? '/explore/' + tab.slug : '/explore'" exact>{{ tab.name }}</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/explore/recent" exact>{{ $t('Most Recent') }}</nuxt-link>
            </li>
          </ul>
        </nav>
      </header>

      <nuxt-child/>
    </explore-view>
  </AppLayout>
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
    position: relative
    top: -1px

    background: #fff
    border-bottom: 1px solid #eee

    nav
      margin: 0 auto
      max-width: 900px
      padding: 0 $baseline

      @media (max-width: $mobile)
        padding: 0 $baseline/4

      ul
        @media (max-width: $mobile)
          display: block

          white-space: nowrap
          overflow-x: auto
          -webkit-overflow-scrolling: touch

      li
        display: inline-block
        margin-right: $baseline

        @media (max-width: $mobile)
          margin-right: $baseline / 2

      a
        display: block

        color: #777

        line-height: $baseline * 1.5

        &:hover,
        &:focus,
          color: #000

        &.nuxt-link-active
          color: #000

          font-weight: 600


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
      -webkit-overflow-scrolling: touch

      newspaper-widget-view,
      issue-widget-view
        min-width: 200px

</style>
