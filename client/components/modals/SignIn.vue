<template>
  <DialogWindow :closeModal="closeModal" :cancelClosingOnBackground="true">
    <modal-dialog role="dialog" @click.stop class="sign-in">
      <header>
        <h1>{{ $t('Sign In') }}</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <main>
        <form @submit.prevent="login">
          <div>
            <label for="username">{{ $t('Username') }}</label>
            <input name="username" id="username" v-model="username" />
          </div>

          <div>
            <label for="password">{{ $t('Password') }}</label>
            <input name="password" id="password" type="password" v-model="password" />
          </div>

          <button type="submit">{{ $t('Sign in') }}</button>

          <div class="login--error-message" v-if="invalidCredentials">
            {{ $t('Wrong username or password') }}
          </div>
        </form>

        <div class="login--forgot-password">
          <button @click="openForgotPassword()" v-if="!isForgotPasswordOpen">
            {{ $t('Forgot password?') }}
          </button>

          <p v-else>
            {{ $t('Contact us on') }} 
            <a href="mailto:info@kairly.com?subject=Zapomenuté heslo`&body=Vaše uživatelské jméno nebo email: [vyplňte]">info@kairly.com</a>.
          </p>
        </div>
      </main>
    </modal-dialog>
  </DialogWindow>
</template>


<script>
import DialogWindow from '@/components/modals/DialogWindow'

export default {
  name: 'JoinUsDialog',

  props: {
    closeModal: Function
  },

  components: {
    DialogWindow
  },

  data() {
    return {
      invalidCredentials: false,
      username: null,
      password: null,
      isForgotPasswordOpen: false
    }
  },

  methods: {
    openForgotPassword() {
      this.isForgotPasswordOpen = true

      this.$ga.event({
        eventCategory: 'Authentication',
        eventAction: 'Open forgot password'
      })
    },

    async login() {
      this.invalidCredentials = false
      const { username, password } = this

      try {
        await this.$auth.loginWith('local', {
          data: { username, password }
        })
        this.$router.push("/")
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
modal-dialog.sign-in
  background: #eee

  main
    padding: $baseline

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
  button
    +button-text

    color: #777

    font-weight: 400
    text-decoration: underline

    &::after
      display: none

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
</style>
