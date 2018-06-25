<template>
  <sign-up-wrapper>
    <homepage--cover>
      <h1>Kairly</h1>

      <p>We stand for exceptional journalism<br /> &amp; great reading experience.</p>
    </homepage--cover>
    <main>
      <h1>Sign Up</h1>

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

      <div class="error">{{ error }}</div>
    </main>
  </sign-up-wrapper>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'SignUp',

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
          this.error = response.body.error
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



sign-up-wrapper
  homepage--cover
    height: 180px

  main
    width: 800px
    margin: 0 auto

    div
      margin: 10px 0

    .error
      color: red

</style>
