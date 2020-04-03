<template>
  <DialogWindow
    v-if="active"
    custom-class="sign-in"
    ignore-background-click
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Sign In') }}</h1>
    </template>

    <form @submit.prevent="login">
      <div>
        <label for="username">{{ $t('Username') }}</label>
        <input id="username" v-model="username" name="username">
      </div>

      <div>
        <label for="password">{{ $t('Password') }}</label>
        <input id="password" v-model="password" name="password" type="password">
      </div>

      <button type="submit">{{ $t('Sign in') }}</button>

      <div v-if="invalidCredentials" class="login--error-message">
        {{ $t('Wrong username or password') }}
      </div>
    </form>

    <div class="login--forgot-password">
      <nuxt-link to="reset-password">{{ $t('Forgot password?') }}</nuxt-link>
    </div>

    <div class="login--signup">
      Don't have account yet? <nuxt-link to="/signup">Sign up</nuxt-link>
    </div>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'SignInModal',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin],

  data () {
    return {
      invalidCredentials: false,
      username: null,
      password: null,
      isForgotPasswordOpen: false
    }
  },

  methods: {
    async login () {
      this.invalidCredentials = false
      const { username, password } = this

      try {
        await this.$auth.loginWith('local', {
          data: { username, password }
        })
        this.$router.push('/')
        this.$ga.event({
          eventCategory: 'Authentication',
          eventAction: 'Sign in',
          eventLabel: 'Success'
        })

        this.$ga.set('dimension1', 'yes')
      } catch (e) {
        this.invalidCredentials = true
        this.$ga.event({
          eventCategory: 'Authentication',
          eventAction: 'Sign in',
          eventLabel: 'Invalid credentials'
        })
      }
    }
  }
}
</script>

<style lang="sass">
//- Imports -//
@import './styles/components/buttons'

//- Styles -//
.modal-dialog.sign-in
  background: #f5f5f5

  main
    padding: $baseline $baseline 0 $baseline

  div
    margin-bottom: $baseline / 2

    &:last-of-type
      margin-bottom: 0

  form input
    border-radius: 5px
    box-sizing: border-box
    height: $baseline * 1.5
    padding: 0 $baseline/4
    width: 100%

    border: 1px solid #ccc

    font-size: $fs-0
    font-family: $ff-sans

  form button
    border-radius: 5px
    height: $baseline * 1.5
    margin-top: $baseline / 2
    width: 100%

    background: $c-base
    border: 0
    color: #fff

    cursor: pointer
    font-size: $fs-0
    font-family: $ff-sans

    &:focus,
    &:hover
      background: darken($c-base, 10%)

//- Error message invalid credentials
.login--error-message
  padding: $baseline/4
  margin-top: $baseline / 2

  color: $c-red

//- Forgot password
.login--forgot-password
  margin-top: $baseline / 2
  text-align: center

  //- forgot password text button
  a
    color: #777

    text-decoration: underline

    &:hover,
    &:focus
      color: #333
      text-decoration: none

  p a
    color: $c-base

    text-decoration: underline

    &:hover,
    &:focus
      text-decoration: none

//- Signup
.login--signup
  margin: 0 (-$baseline)
  padding: $baseline/2 $baseline

  background: #fff

  text-align: center

  a
    color: $c-base
    text-decoration: underline

    &:hover,
    &:focus
      text-decoration: none
</style>
