<template>
  <app-header-view>
    <div>
      <app-header--nav role="navigation">
        <ul v-if="user">
          <li class="home"><nuxt-link :to="{name: 'index'}" exact><span>Home</span></nuxt-link></li>
          <li class="my-subscription"><nuxt-link :to="{name: 'subscription-newspapers'}"><span>My Subscription</span></nuxt-link></li>
          <li class="my-newspapers"><nuxt-link :to="{name: 'newspapers'}"><span>My Newspapers</span></nuxt-link></li>
          <li class="explore"><nuxt-link :to="{name: 'explore'}"><span>Explore</span></nuxt-link></li>
        </ul>
        </app-header--nav>

        <app-header--user-profile v-if="user">
          <h3><nuxt-link :to="{name: 'author', params: {author: user.id}}">{{ user.name }}</nuxt-link></h3>
          <nuxt-link :to="{name: 'author', params: {author: user.id}}">
            <img
              v-if="user.picture"
              :src="user.picture || '~/assets/user.png'"
              :alt="user.name"
            />

            <img
              v-else
              src="~/assets/user.png"
              :alt="user.name"
            />
          </nuxt-link>
          <button-icon v-on:click="isDropDownMenuOpen = true"></button-icon>
        </app-header--user-profile>

        <app-header--user-profile-menu
          v-if="user && isDropDownMenuOpen"
          v-on-clickaway="() => isDropDownMenuOpen = false">
          <ul>
            <li class="my-subscription"><nuxt-link :to="{name: 'subscription-newspapers'}"><span>My Subscription</span></nuxt-link></li>
            <li class="my-newspapers"><nuxt-link :to="{name: 'newspapers'}"><span>My Newspapers</span></nuxt-link></li>
            <li class="explore"><nuxt-link :to="{name: 'explore'}"><span>Explore</span></nuxt-link></li>
            <li><nuxt-link :to="{name: 'user-settings'}"><span>Settings</span></nuxt-link></li>
            <li><a href="" v-on:click.prevent="isTutorialOpen=true">Help</a></li>
            <li><a href="" v-on:click.prevent="logout">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>
    </div>

    <portal to="modal" v-if="isTutorialOpen">
      <tutorial-modal :closeModal="closeTutorial"></tutorial-modal>
    </portal>

  </app-header-view>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapGetters, mapActions } from 'vuex'
import store from '@/store'

import TutorialModal from '@/components/modals/Tutorial'

export default {
  name: 'AppHeader',

  components: {
    TutorialModal
  },

  directives: {
    onClickaway
  },

  data: function() {
    return {
      username: null,
      password: null,
      isDropDownMenuOpen: false,
      isTutorialOpen: false
    }
  },

  computed: mapGetters(['user', 'loadingUser']),

  methods: {
    ...mapActions(['login', 'logout']),

    closeTutorial() {
      this.isTutorialOpen = false
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

  background: #fff
  border-bottom: 1px solid #eee
  color: #555

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

    color: #555

    &:focus,
    &:hover
      background: #eee

    &.nuxt-link-active
      background: #eee

    @media (max-width: $mobile)
      padding: 0 $baseline*0.75

      span
        display: none

  @media (max-width: $mobile)
    .my-subscription,
    .my-newspapers,
    .explore
      display: none


  li a::before
    +fa-icon()

    margin-right: $baseline / 4

  li.home a::before
    content: $fa-var-home

  li.my-subscription a::before
    content: $fa-var-clock-o

  li.my-newspapers a::before
    content: $fa-var-newspaper-o

  li.explore a::before
    content: $fa-var-hashtag

  @media (max-width: $mobile)
    li a::before
      position: relative
      top: 5px

      font-size: $fs-2
      margin-right: 0


//- User Profile
app-header--user-profile
  cursor: pointer

  //- profile name
  h3
    display: inline-block
    margin-right: $baseline / 4

    @media (max-width: $mobile)
      display: none

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
      background: #eee

    &::before
      content: $fa-var-chevron-down


//- User Profile Menu
app-header--user-profile-menu
  position: absolute
  right: 0
  top: $baseline * 2
  z-index: 100000000
  min-width: 120px
  +box-shadow

  font-size: $fs--2
  line-height: $baseline

  ul
    +blur

  a
    display: block
    padding: $baseline / 4

    color: #555

    &:focus,
    &:hover
      background: #fff

  .my-subscription,
  .my-newspapers,
  .explore
    display: none

    @media (max-width: $mobile)
      display: block


</style>
