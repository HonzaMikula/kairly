<template>
  <AppLayout :name="$t('Explore')">
    <div
      class="explore-view"
      :class="$route.name === 'explore-recent' ? 'recent' : $route.params.tab"
    >
      <header>
        <nav>
          <ul>
            <li v-for="tab in tabs" :key="tab.slug">
              <nuxt-link :to="{name: 'explore-tab', params: {tab: tab.slug}}">{{ tab[$i18n.locale] || tab.en }}</nuxt-link>
            </li>
            <li>
              <nuxt-link to="/explore/recent" exact>{{ $t('Most Recent') }}</nuxt-link>
            </li>
          </ul>
        </nav>
      </header>

      <nuxt-child/>
    </div>
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
.explore-view

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
</style>
