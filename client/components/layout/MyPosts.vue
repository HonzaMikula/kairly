<template>
  <AppLayout :name="$t('My posts')">
    <div class="my-posts">
      <header>
        <nav>
          <nuxt-link to="/posts" exact>{{ $t('Drafts') }}</nuxt-link>
          <nuxt-link to="/posts/published">{{ $t('Published posts') }}</nuxt-link>
        </nav>

        <div class="my-posts--create-post">
          <nuxt-link to="/posts/create/article">{{ $t('Create post') }}</nuxt-link>
        </div>
      </header>

      <slot />
    </div>
  </AppLayout>
</template>

<script>


import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'MyPosts',

  head() {
    return {
      title: this.$t('My Posts – Kairly')
    }
  },

  components: {
    AppLayout
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- MY POSTS -//
.my-posts
  display: block
  box-sizing: border-box
  max-width: 900px
  margin: $baseline auto

  @media (max-width: $mobile)
    padding: 0 $baseline/4

  //- header
  > header
    display: flex

    nav
      flex: 1
      margin-bottom: $baseline

      @media (max-width: $mobile)
        margin-bottom: $baseline / 2


      a
        display: inline-block
        margin-right: $baseline

        color: $c-base

        font-size: $fs-3
        font-weight: 600

        @media (max-width: $mobile)
          font-size: $fs-1
          margin-right: $baseline / 2

        &.nuxt-link-active
          border-bottom: 2px solid #000
          color: #000

//- Create Post button
.my-posts--create-post

  a
    +button

    @media (max-width: $mobile)
      height: $baseline
      padding: 0 $baseline/4

      font-size: $fs--1
      line-height: $baseline
</style>
