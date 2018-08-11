<template>
  <sign-up-page>
    <div>
      <header>
        <h1>Kairly</h1>
        <p>Sign up to help with resurrection of exceptional journalism.</p>
      </header>

      <main>
        <div class="error" v-if="error">{{ error }}</div>

        <div>
          <input placeholder="Username" v-model="username">
        </div>
        <div>
          <input placeholder="Email" v-model="email">
        </div>
        <div>
          <input type="password" placeholder="Password" v-model="password">
        </div>

        <button @click="submit">Sign Up</button>
      </main>
    </div>
  </sign-up-page>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'SignUp',

  metaInfo: {
    title: 'Sign Up'
  },

  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: null
    }
  },

  methods: {
    submit() {
      const { username, email, password }  = this
      api.signUp({ username, email, password })
      .then(
        () => {
          api.createToken(username, password)
          .then(this.getProfile)
          //.then(() => this.$router.push({ path: '/' }))
          // workaround for now, make reload
          .then(() => window.location = '/')
        },
        ({response}) => {
          this.error = response.data.error
        }
      )
    }
  },

  created() {
    // TODO redirect to home when user is already logged in
  }
}
</script>

<style lang="sass">
sign-up-page
  display: flex
  align-items: center
  justify-content: center

  height: 100vh
  width: 100vw

  background: url(../../assets/homepage/hero.png) center center no-repeat
  background-size: cover

  //- Header
  header
    margin-bottom: $baseline * 2

    color: #fff
    text-shadow: 1px 1px 1px #000

    font-family: $ff-serif

    h1
      margin-bottom: $baseline

      font-size: 50px
      text-align: center

    p
      font-size: $fs-2


  //- Form
  main
    padding: $baseline
    width: 300px
    margin: 0 auto

    backdrop-filter: blur(10px) saturate(125%)
    background: rgba(0, 0, 0, 0.2)

    //- Heading
    h2
      margin-bottom: $baseline

      color: #fff

      font-size: $fs-2
      text-align: center

    //- Form Fields
    input
      box-sizing: border-box
      height: $baseline * 1.5
      padding: 0 $baseline/4
      width: 100%

      background: rgba(255, 255, 255, 0.7)
      border: 0
      border-radius: 10px

      font-family: $ff-sans
      font-size: $fs-0

      &:focus
        background: #fff

    //- Button
    button
      +subscribe-button

      height: $baseline * 1.5
      width: 100%

      background: $c-base
      color: #fff

      font-family: $ff-sans

      &:focus,
      &:hover
        background: darken($c-base, 10%)
        border: 1px solid darken($c-base, 10%)


    div
      margin-bottom: $baseline

    .error
      padding: $baseline / 4

      background: lighten($c-red, 50%)
      border: 1px dashed $c-red
      color: #000

      text-align: center

</style>
