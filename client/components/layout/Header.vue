<template>
  <header class="app-header">
    <div>
      <h1 class="app-header--logo"><nuxt-link :to="{name: 'index'}" exact>Kairly</nuxt-link></h1>
      <nav class="app-header--navigation">
        <ul v-if="user">
          <li class="home">
            <nuxt-link :to="{name: 'index'}" exact title="Home">
              <span>Home</span>
            </nuxt-link>
          </li>

          <li class="subscription">
            <nuxt-link :to="{name: 'subscription-newspapers'}" title="Subscriptions">
              <span>Subscriptions</span>
            </nuxt-link>
          </li>

          <li class="newspapers">
            <nuxt-link :to="{name: 'newspapers'}" title="Newspapers">
              <span>Newspapers</span>
            </nuxt-link>
          </li>

          <li class="new-post">
            <nuxt-link :to="{name: 'posts'}" title="New post">
              <span>New post</span>
            </nuxt-link>
          </li>

          <li class="explore">
            <nuxt-link :to="{name: 'explore-tab'}" title="Explore">
              <span>Explore</span>
            </nuxt-link>
          </li>
        </ul>
      </nav>

      <nav class="app-header--user-profile" v-if="user">
        <img v-if="user.picture" :src="user.picture" :alt="user.name" />
        <img v-else src="~assets/user.png" :alt="user.name"/>
        <button-icon
          @click="isDropDownMenuOpen = true"
          :class="{'is-active': isDropDownMenuOpen}"
        />
      </nav>

      <nav class="app-header--user-profile-menu"
        v-if="user && isDropDownMenuOpen"
        v-on-clickaway="() => isDropDownMenuOpen = false">
        <ul>
          <li class="user-name">{{user.name}}</li>
          <li><nuxt-link :to="{name: 'author', params: {author: user.id}}">Profile</nuxt-link></li>
          <li><nuxt-link :to="{name: 'user-settings'}"><span>Settings</span></nuxt-link></li>
          <li class="divider"></li>
          <li class="my-subscription"><nuxt-link :to="{name: 'subscription-newspapers'}"><span>Subscriptions</span></nuxt-link></li>
          <li class="my-newspapers"><nuxt-link :to="{name: 'newspapers'}"><span>Newspapers</span></nuxt-link></li>
          <li><nuxt-link to="/posts">New post</nuxt-link></li>
          <li class="explore"><nuxt-link :to="{name: 'explore-tab'}"><span>Explore</span></nuxt-link></li>
          <li class="divider"></li>
          <li><a href="" @click.prevent="logout">Logout</a></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapState } from 'vuex'
import store from '@/store'

export default {
  name: 'AppHeader',

  directives: {
    onClickaway
  },

  data: function() {
    return {
      username: null,
      password: null,
      isDropDownMenuOpen: false
    }
  },

  computed: mapState({
    user: state => state.auth.user
  }),

  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push("/homepage")
    }
  }
}
</script>

<style lang="sass">
//- HEADER -//
.app-header
  display: block
  height: $baseline * 2
  padding: 0 $baseline

  background: #fff
  border-bottom: 1px solid #eee
  color: #555

  line-height: $baseline * 2

  @media (max-width: $mobile)
    padding: 0 $baseline/4 0 0

  //- wrapper
  > div
    position: relative

    display: grid
    grid-template-columns: auto 1fr auto
    margin: 0 auto
    max-width: 900px


//- Main Navigation
.app-header--navigation
  margin-right: auto

  ul
    display: flex

  a
    display: block
    padding: 0 $baseline/2

    color: #555

    &:focus,
    &:hover
      background: #eee

    &.nuxt-link-active
      background: #eee

    @media (max-width: 850px)
      span
        display: none

  @media (max-width: $mobile)
    .home,
    .subscription,
    .newspapers,
    .new-post,
    .explore
      display: none


  li a::before
    +fa-icon()

    font-size: $fs-1
    text-align: center

  li.home a::before
    content: $fa-var-home
    display: none

    @media (max-width: 850px)
      display: inline-block


  li.subscription a::before
    content: $fa-var-calendar
    display: none

    @media (max-width: 850px)
      display: inline-block

  li.newspapers a::before
    content: $fa-var-newspaper-o
    display: none

    @media (max-width: 850px)
      display: inline-block

  li.new-post a::before
    content: $fa-var-pencil-square-o
    display: none

    @media (max-width: 850px)
      display: inline-block

  li.explore a::before
    content: $fa-var-hashtag
    display: none

    @media (max-width: 850px)
      display: inline-block

  @media (max-width: $mobile)
    li a::before
      position: relative
      top: 5px

      font-size: $fs-2
      margin-right: 0


.app-header--logo
  margin-right: $baseline

  font-family: $ff-serif
  font-weight: 600
  font-size: $fs-3
  text-align: center

  @media (max-width: $mobile)
    font-size: $fs-2
    padding-left: $baseline / 4

  a
    color: #000


//- User Profile
.app-header--user-profile
  justify-self: end

  cursor: pointer

  > a
    display: inline-block
    padding: 0 $baseline/2

    color: #000

    &:focus,
    &:hover
      background: #eee

    &.nuxt-link-active
      background: #eee

    @media (max-width: 850px)
      span
        display: none

  //- profile picture
  img
    border-radius: 100%
    height: $baseline * 1.25
    margin-left: $baseline / 4
    width: $baseline * 1.25
    vertical-align: middle

    object-fit: cover

    @media (max-width: 850px)
      margin-left: 0

  //- dropdown button
  button-icon
    display: inline-block
    border-radius: 100%
    height: $baseline * 1.25
    width: $baseline * 1.25

    line-height: $baseline * 1.25
    vertical-align: middle
    text-align: center

    &:focus,
    &:hover,
    &.is-active
      background: #eee

    &::before
      content: $fa-var-chevron-down


//- User Profile Menu
.app-header--user-profile-menu
  position: absolute
  right: 0
  top: $baseline * 2
  z-index: 100000000
  min-width: 120px
  +box-shadow

  font-size: $fs--1
  line-height: $baseline

  ul
    +blur

  a
    display: block
    padding: $baseline / 4 $baseline / 2

    color: #555

    &:focus,
    &:hover
      background: #fff

  //- user name
  .user-name
    font-weight: 600
    padding: $baseline / 4 $baseline / 2

  //- divider
  .divider
    border-top: 1px solid #eee


</style>
