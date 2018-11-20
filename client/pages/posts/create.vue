<template>
  <app-layout>
    <div class="edit-post-view">
      <nav class="create-post">
        <nuxt-link to="/posts/create/article">{{ $t('Write an article') }}</nuxt-link>
        <nuxt-link to="/posts/create/tweet">{{ $t('Write a tweet') }}</nuxt-link>
      </nav>

      <nuxt-child/>
    </div>
  </app-layout>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'CreatePost',

  components: {
    AppLayout
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  }
}
</script>

<style lang="sass">
//- Switcher
.edit-post-view
  box-sizing: border-box
  padding: $baseline 0
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline $baseline/4

  nav
    margin-bottom: $baseline

    font-size: $fs-3

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 600

      &.nuxt-link-active
        color: #000
</style>
