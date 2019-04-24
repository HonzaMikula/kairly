<template>
  <div class="microsite-signup-form">
    <h2>{{ $t('@signupform/heading') }}</h2>
    <p>{{ $t('We are opening the platform for first 125 beta testers.') }}</p>
    <div class="error" v-if="error">{{ error }}</div>

    <div>
      <label>{{ $t('Username') }}</label>
      <input v-model="username">
    </div>
    <div>
      <label>{{ $t('Email') }}</label>
      <input v-model="email" placeholder="@">
    </div>
    <div>
      <label>{{ $t('Password') }}</label>
      <input type="password" v-model="password">
      <p>{{ $t('At least 8 characters') }}</p>
    </div>

    <button @click="submit">{{ $t('Sign Up') }}</button>
  </div>
</template>

<script>
export default {
  name: 'SignUpForm',

  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: null
    }
  },

  methods: {
    async submit() {
      const { username, email, password } = this

      this.$ga.event({
        eventCategory: 'Sign up'
      })

      try {
        const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
        await this.$axios.post('/signup',
          { username, email, password },
          { headers: { 'X-Timezone': timeZone }}
        )
        await this.$auth.loginWith('local', {
          data: { username, password }
        })
        this.$router.push("/")
      } catch (err) {
        if (err.response) {
          this.error = err.response.data.error
        } else {
          this.error = err
        }
      }
    }
  },

  async fetch ({ store, redirect }) {
    if (store.state.auth.loggedIn) {
      redirect('/')
      return
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- SIGN UP FORM -//
.microsite-signup-form
  border-radius: 5px
  padding: $baseline

  background: #fff
  background: rgba(255,255,255,0.95)
  border: 1px solid #ddd

  font-family: $ff-sans

  @media (max-width: $mobile)
    border: 0
    border-radius: 0
    border-top: 1px solid #ddd
    border-bottom: 1px solid #ddd

  //- Heading
  h2
    margin-bottom: $baseline / 4
 
    font-size: $fs-2
    font-weight: 600

  p
    margin-bottom: $baseline / 2
    line-height: 1.42  

  //- Label
  label
    color: #000

  //- Form Fields
  input
    box-sizing: border-box
    height: $baseline * 1.25
    padding: 0 $baseline/4
    width: 100%

    background: #fff
    border: 1px solid #ddd
    border-radius: 5px

    font-family: $ff-sans
    font-size: $fs-0

    &:focus
      background: #fff

  //- Note
  p
    color: #777

    font-size: $fs--1
    text-align: left

  //- Button
  button
    +button(primary, medium)
    width: 100%


  div
    margin-bottom: $baseline / 2

  .error
    color: $c-red

    list-style: disc

    text-align: left

</style>
