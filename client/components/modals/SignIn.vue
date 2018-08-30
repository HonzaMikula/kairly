<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="join-us">
      <header>
        <h1>Sign in</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <div>
        <form v-on:submit.prevent="login">
          <div>
            <input name="username" placeholder="Username" v-model="username" />
          </div>

          <div>
            <input name="password" placeholder="Password" type="password" v-model="password" />
          </div>

          <button type="submit">Sign In</button>

          <div class="login--error-message" v-if="invalidCredentials">
            Wrong login or password
          </div>
        </form>
      </div>
    </modal-dialog>
  </dialog-window>
</template>


<script>
import DialogWindow from '@/components/modals/Dialog'

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
      password: null
    }
  },

  methods: {
    async login() {
      this.invalidCredentials = false
      const { username, password } = this
      try {
        await this.$auth.loginWith('local', {
          data: { username, password }
        })
        this.$router.push("/")
      } catch (e) {
        this.invalidCredentials = true
      }
    }
  }
}
</script>

<style lang="sass">
modal-dialog.join-us

  > div
    padding: $baseline

  input
    box-sizing: border-box
    height: $baseline * 1.5
    padding: 0 $baseline/4
    margin-bottom: $baseline / 2
    width: 100%

    font-size: $fs-0
    font-family: $ff-sans


  button
    height: $baseline * 1.25
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


  .login--error-message
    padding: $baseline/4
    margin-top: $baseline / 2

    color: $c-red

</style>
