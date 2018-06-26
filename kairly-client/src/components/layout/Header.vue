<template>
  <app-header-view>
    <div>
      <app-header--nav role="navigation">
        <ul v-if="user">
          <li class="home"><router-link :to="{name: 'timeline'}" exact>Home</router-link></li>
          <li class="my-subscription"><router-link :to="{name: 'subscription'}">My Subscription</router-link></li>
          <li class="my-editions"><router-link :to="{name: 'author-editions', params: {authorId: user.id}}">My Editions</router-link></li>
          <li class="explore"><router-link :to="{name: 'explore'}">Explore</router-link></li>
        </ul>
        </app-header--nav>

        <app-header--user-profile v-if="user">
          <h3><router-link :to="{name: 'author', params: {authorId: user.id}}">{{ user.name }}</router-link></h3>
          <img src="../../assets/user.png" :alt="user.name"/>
          <!--
            Gravatar url handles default itself (it can generate 404 url or some dafault),
            but it is problematic handle it on client side identify default and replace it with own default
          -->
          <!--img :src="user.picture" :alt="user.name"/-->
          <button-icon v-on:click="openDropDownMenu"></button-icon>
        </app-header--user-profile>

        <app-header--user-profile-menu v-if="user && isDropDownMenuOpen" v-on:mouseleave="closeDropDownMenu">
          <ul>
            <li><a href="" v-on:click.prevent="isTutorialOpen=true">Help</a></li>
            <li><a href="" v-on:click.prevent="logout">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>
    </div>

    <portal to="modal" v-if="isTutorialOpen">
      <tutorial-modal :onClose="closeTutorial"></tutorial-modal>
    </portal>

  </app-header-view>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import store from '@/store'

import TutorialModal from '@/components/modals/Tutorial'

export default {
  name: 'AppHeader',
  data: function() {
    return {
      username: null,
      password: null,
      isDropDownMenuOpen: false,
      isTutorialOpen: false
    }
  },

  components: {
    TutorialModal
  },

  computed: mapGetters(['user', 'loadingUser']),

  methods: {
    ...mapActions(['login', 'logout']),

    openDropDownMenu() {
      this.isDropDownMenuOpen = true
      this.$forceUpdate()
    },

    closeDropDownMenu() {
      this.isDropDownMenuOpen = false
      this.$forceUpdate()
    },

    closeTutorial() {
      this.isTutorialOpen = false
      this.$forceUpdate()
    }
  }
}
</script>

<style lang="sass">
//- HEADER -//
app-header-view
  display: block
  height: $baseline * 2
  padding: 0 $baseline

  background: $c-base
  color: #fff

  font-size: $fs--1
  line-height: $baseline * 2

  @media (max-width: $mobile)
    padding: 0 $baseline/4 0 0

  //- wrapper
  > div
    position: relative

    display: flex
    margin: 0 auto
    max-width: 900px


//- Main Navigation
app-header--nav
  margin-right: auto

  ul
    display: flex

  a
    display: block
    padding: 0 $baseline / 2

    color: #fff

    &:focus,
    &:hover
      background: darken($c-base, 10%)

    &.is-active
      background: darken($c-base, 15%)

    @media (max-width: $mobile)
      padding: 0 $baseline/4



  li a::before
    +fa-icon()

    margin-right: $baseline / 4

  li.home a::before
    content: $fa-var-home

  li.my-subscription a::before
    content: $fa-var-clock-o

  li.my-editions a::before
    content: $fa-var-newspaper-o

  li.explore a::before
    content: $fa-var-hashtag

  @media (max-width: $mobile)
    li a::before
      margin-right: 0

      content: '' !important


//- User Profile
app-header--user-profile
  cursor: pointer

  //- profile name
  h3
    display: inline-block
    margin-right: $baseline / 4

    a
      color: #fff

  //- profile picture
  img
    border-radius: 100%
    height: $baseline * 1.25
    width: $baseline * 1.25
    vertical-align: middle

    object-fit: cover

  //- dropdown button
  button-icon
    display: inline-block
    border-radius: 100%
    height: $baseline * 1.25
    margin-left: $baseline / 4
    width: $baseline * 1.25

    line-height: $baseline * 1.25
    vertical-align: middle
    text-align: center

    &:focus,
    &:hover
      background: darken($c-base, 10%)

    &::before
      content: $fa-var-chevron-down


//- User Profile Menu
app-header--user-profile-menu
  position: absolute
  right: 0
  top: $baseline * 2
  z-index: 1

  padding: $baseline / 4 0
  min-width: 150px

  background: #fff
  border: 1px solid #eee
  box-shadow: 1px 1px 3px #999

  font-size: $fs--2
  line-height: $baseline

  a
    display: block
    padding: 0 $baseline / 2

    color: #555

    &:focus,
    &:hover
      background: #eee


</style>
