<template>
  <header class="app-header-public">
    <div>
      <h1><a href="/">Kairly</a></h1>

      <p>We aim for exceptional journalism</p>

      <nav>
        <ul>
          <li><a href="" v-on:click.prevent="isJoinUsModalOpen = true">Join us</a></li>
          <li><a href="" v-on:click.prevent="isSignInModalOpen = true">Sign In</a></li>
        </ul>
      </nav>
    </div>

    <portal to="modal" v-if="isJoinUsModalOpen">
      <JoinUsModal :closeModal="closeModals"></JoinUsModal>
    </portal>

    <portal to="modal" v-if="isSignInModalOpen">
      <SignInModal :closeModal="closeModals"></SignInModal>
    </portal>
  </header>
</template>

<script>
import JoinUsModal from '@/components/modals/JoinUs'
import SignInModal from '@/components/modals/SignIn'

export default {
  name: 'AppHeaderPublic',

  components: {
    JoinUsModal,
    SignInModal
  },

  data() {
    return {
      isJoinUsModalOpen: null,
      isSignInModalOpen: null
    }
  },

  methods: {
    closeModals() {
      this.isJoinUsModalOpen = null
      this.isSignInModalOpen = null
    }
  }
}
</script>

<style lang="sass">
//- HEADER -//
.app-header-public
  display: block
  height: $baseline * 2
  padding: 0 $baseline

  background: #fff
  border-bottom: 1px solid #eee
  color: #555

  line-height: $baseline * 2

  @media (max-width: $mobile)
    padding: 0 $baseline/2

  //- wrapper
  > div
    position: relative

    margin: 0 auto
    max-width: 900px

  //- logo
  h1
    font-family: $ff-serif
    font-weight: 600
    font-size: $fs-3
    text-align: center

    a
      color: #000

    @media (max-width: $mobile)
      font-size: $fs-2
      text-align: left

  //- motto
  p
    position: absolute
    left: 0
    top: 0

    font-family: $ff-serif
    font-size: $fs-0

    @media (max-width: $mobile)
      display: none


  //- join us / sign in
  nav
    position: absolute
    right: 0
    top: 0

    li
      display: inline-block
      margin-left: $baseline

    a
      color: $c-base


</style>
