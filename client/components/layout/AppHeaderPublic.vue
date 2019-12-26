<template>
  <header class="app-header-public">
    <div>
      <h1><a href="/">Kairly</a></h1>

      <nav class="app-header-public--menu">
        <ul>
          <li><nuxt-link to="/platform/readers">{{ $t('About') }}</nuxt-link></li>
          <li><nuxt-link to="/features/rss-reader">{{ $t('Features') }}</nuxt-link></li>
          <li><nuxt-link to="/explore/news">{{ $t('Explore') }}</nuxt-link></li>
          <li><nuxt-link to="/janmikula/kairly">{{ $t('Our newspaper (blog)')}}</nuxt-link></li>
        </ul>
      </nav>

      <nav class="app-header-public--controls">
        <ul>
          <li class="signup"><nuxt-link to="/signup">{{ $t('Create account') }}</nuxt-link></li>
          <li class="signin"><a href="" @click.prevent="openSignInModal()">{{ $t('Sign in') }}</a></li>
        </ul>
        <button class="hamburger-menu" @click="openMobileMenu()"></button>
      </nav>
    </div>

    <nav class="app-header-public--submenu">
      <template v-if="topRoute == 'platform'">
        <span>{{ $t('For who?') }}</span>

        <ul>
          <li><nuxt-link to="/platform/readers">{{ $t('Readers') }}</nuxt-link></li>
          <li><nuxt-link to="/platform/journalists">{{ $t('Journalists and bloggers') }}</nuxt-link></li>
          <li><nuxt-link to="/platform/publishers">{{ $t('Publishers') }}</nuxt-link></li>
          <li><nuxt-link to="/platform/think-tanks">{{ $t('Think-tanks and NGOs') }}</nuxt-link></li>
        </ul>
      </template>

      <template v-else-if="topRoute == 'features'">
        <ul>
          <li><nuxt-link to="/features/rss-reader">{{ $t('RSS reader') }}</nuxt-link></li>
        </ul>
      </template>
    </nav>

    <nav
      class="app-header-public--mobile-menu"
      v-if="isMobileMenuOpen"
      v-on-clickaway="() => openMobileMenu()">
      <ul>
        <li><nuxt-link to="/">{{ $t('Home') }}</nuxt-link></li>
        <li><nuxt-link to="/platform/readers">{{ $t('About platform') }}</nuxt-link></li>
        <li><nuxt-link to="/features/rss-reader">{{ $t('Features') }}</nuxt-link></li>
        <li><nuxt-link to="/explore/news">{{ $t('Explore') }}</nuxt-link></li>
        <li><nuxt-link to="/janmikula/kairly">{{ $t('Our newspaper (blog)')}}</nuxt-link></li>
        <li><nuxt-link to="/signup">{{ $t('Create account') }}</nuxt-link></li>
      </ul>
    </nav>

    <SignInModal
      :active.sync="isSignInModalOpen"
    />
  </header>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import SignInModal from '@/components/modals/SignInModal'

export default {
  name: 'AppHeaderPublic',

  directives: {
    onClickaway
  },

  components: {
    SignInModal
  },

  data() {
    return {
      isSignInModalOpen: false,
      isMobileMenuOpen: false,
    }
  },

  computed: {
    topRoute() {
      const routes = this.$route.path.split('/')

      if (routes[1] == '') {
        return '/'
      }
      return routes[1]
    }
  },

  methods: {
    openSignInModal() {
      this.isSignInModalOpen = true
      this.$ga.event({
        eventCategory: 'Authentication',
        eventAction: 'Open Sign in modal'
      })
    },

    openMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- HEADER -//
.app-header-public
  display: block
  padding: 0 $baseline

  background: #fff
  border-bottom: 1px solid #eee
  color: #555

  font-size: $fs-1
  line-height: $baseline * 2

  @media (max-width: $mobile)
    padding: 0 $baseline/2

  //- wrapper
  > div
    position: relative
    display: flex

    margin: 0 auto
    max-width: 900px

  //- logo
  h1
    display: inline-block

    font-family: $ff-serif
    font-weight: 600
    font-size: $fs-3

    a
      display: block
      padding-right: $baseline

      color: #000

    @media (max-width: $mobile)
      font-size: $fs-2
      text-align: left


  //- Get Involved
  .app-header-public--menu
    margin-right: auto

    ul
      display: flex

      @media (max-width: $mobile)
        display: none

    li
      list-style: none
      a
        display: block
        border-radius: 5px
        padding: 0 $baseline/2
        margin-top: $baseline / 4
        margin-right: $baseline / 4

        color: #555

        line-height: $baseline * 1.5


        &:focus,
        &:hover,
        &.nuxt-link-active
          background: #eee

    @media (max-width: $mobile)
      margin-right: $baseline / 2

.app-header-public--mobile-menu
  position: absolute
  top: $baseline * 2
  right: 0
  z-index: 1000000

  box-sizing: border-box
  padding: 0 $baseline/2

  background: #fff
  border: 1px solid #eee
  border-top: 0

  line-height: $baseline

  a
    display: block
    padding: $baseline/4 0

    color: $c-base

    &:active,
    &.nuxt-link-active
      color: #000
      font-weight: 600

    &.nuxt-link-exact-active
      color: #000 !important
      font-weight: 600 !important

  li:first-of-type a.nuxt-link-active
      color: $c-base
      font-weight: 400



.app-header-public--submenu
  margin: 0 auto
  max-width: 900px
  padding: 0 $baseline

  font-size: $fs-0
  font-style: italic

  @media (max-width: $mobile)
    padding: 0

  > span
    margin-right: $baseline

    @media (max-width: $mobile)
      display: none

  ul
    display: inline-block

    font-style: normal

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


//- Sign In
.app-header-public--controls
  display: flex
  align-items: center
  margin-left: auto

  ul
    display: flex

    @media (max-width: $mobile)
      .signup
        display: none

      .signin
        margin-top: 0
        margin-right: 0

        a
          margin-top: 0
          margin-right: 0

  li
    list-style: none
    a
      display: block
      border-radius: 5px
      padding: 0 $baseline/2
      margin-top: $baseline / 4
      margin-right: $baseline / 4

      color: #555

      line-height: $baseline * 1.5


      &:focus,
      &:hover,
      &.nuxt-link-active
        background: #eee

    @media (max-width: $mobile)
      margin-right: $baseline / 2

  //- hamburger menu for mobile
  .hamburger-menu
    +button-icon($fa-var-bars)
    display: none
    margin-left: $baseline / 4

    @media (max-width: $mobile)
      display: block





</style>
