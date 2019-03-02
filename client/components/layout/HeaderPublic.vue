<template>
  <header class="app-header-public">
    <div>
      <h1><a href="/">Kairly</a></h1>

      <nav class="app-header-public--get-involved" v-on-clickaway="() => isDropdownOpen = false">
        <button @click.prevent="isDropdownOpen = !isDropdownOpen">{{ $t('Get involved as') }}</button>

        <ul v-if="isDropdownOpen == true">
          <li>{{ $t('Reader') }}</li>
          <li><nuxt-link to="/journalists">{{ $t('Journalist or blogger') }}</nuxt-link></li>
          <li><nuxt-link to="/publishers">{{ $t('Publisher') }}</nuxt-link></li>
          <li>{{ $t('Think-tank or NGO') }}</li>
        </ul>
      </nav>

      <nav class="app-header-public--sign-in">
        <a href="" @click.prevent="isSignInModalOpen = true">{{ $t('Sign In') }}</a>
      </nav>
    </div>

    <portal to="modal" v-if="isSignInModalOpen">
      <SignInModal :closeModal="closeModals"></SignInModal>
    </portal>
  </header>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import JoinUsModal from '@/components/modals/JoinUs'
import SignInModal from '@/components/modals/SignIn'

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
      isDropdownOpen: null,
      isSignInModalOpen: null
    }
  },

  methods: {
    closeModals() {
      this.isDropdownOpen = null
      this.isSignInModalOpen = null
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
  height: $baseline * 2
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
  .app-header-public--get-involved
    margin-left: auto
    margin-right: $baseline

    @media (max-width: $mobile)
      margin-right: $baseline / 2

    //- get involved button
    button
      +button

      padding-right: $baseline /2

      @media (max-width: $mobile)
        padding: 0 $baseline/2
        font-size: $fs--1

        &::after
          content: none

      &::after
        +fa-icon()
        @extend .fas

        margin-left: $baseline / 2

        content: fa-content($fa-var-caret-down)

    //- dropdown
    ul
      position: absolute
      top: ($baseline * 2)
      z-index: 1

      border-radius: 0 0 5px 5px
      padding: $baseline / 2 $baseline

      background: #fff
      border: 1px solid #eee
      +box-shadow

      line-height: 1.42

      @media (max-width: $mobile)
        left: 50%
        transform: translate(-50%,0)

    li
      margin-bottom: $baseline / 2

      white-space: nowrap

      &:last-of-type
        margin-bottom: 0

      a
        color: #777

        &.nuxt-link-active
          color: #000

          font-weight: 600

        &:hover,
        &:focus
          color: #000


  //- Sign In
  .app-header-public--sign-in
    a
      +button(secondary)

      @media (max-width: $mobile)
        padding: 0 $baseline/2
        font-size: $fs--1

        white-space: nowrap




</style>
