<template>
  <app-layout>
    <div class="my-posts">
      <header>
        <nav>
          <nuxt-link to="/posts" exact>Drafts</nuxt-link>
          <nuxt-link to="/posts/published">Published posts</nuxt-link>
        </nav>

        <div class="my-posts--create-post">
          <nuxt-link to="/posts/create/article">Create a post</nuxt-link>
        </div>
      </header>

      <slot />
    </div>
  </app-layout>
</template>

<script>


import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'Posts',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
    }
  },

  components: {
    AppLayout
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  },
}
</script>

<style lang="sass">
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
    margin-bottom: $baseline / 2

    nav
      flex: 1
      margin-bottom: $baseline

      font-size: $fs-3

      a
        display: inline-block
        margin-right: $baseline

        color: $c-base

        font-weight: 600

        &.nuxt-link-active
          color: #000

    .my-posts--create-post a
      +subscribe-button

      display: inline-block
      height: $baseline * 1.25

      border-radius: $baseline*0.75
      background: $c-base
      color: #fff

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.25

      &:focus,
      &:hover
        background: darken($c-base, 10%)
</style>
