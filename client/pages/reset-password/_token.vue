<template>
  <AppLayout>
    <main class="reset-password-token-view">
      <h1>{{ $t('Change password') }}</h1>
      <p>You forgot your password. Here you can change it.</p>
      <form
        @submit.prevent="submit"
      >
        <div>
          <label for="newPassword">{{ $t('New password') }}</label>
          <input
            id="newPassword"
            v-model="newPassword1"
            type="password"
          >
        </div>

        <div>
          <label for="newPassword2">{{ $t('New password again') }}</label>
          <input
            id="newPassword2"
            v-model="newPassword2"
            type="password"
          >
        </div>

        <button type="submit">{{ $t('Change password') }}</button>
      </form>
    </main>
  </AppLayout>
</template>

<script>
import { mapMutations } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'ResetPasswordForm',

  auth: false,

  components: {
    AppLayout,
  },

  mixins: [ErrorHandler],

  data () {
    return {
      newPassword1: '',
      newPassword2: ''
    }
  },

  methods: {
    ...mapMutations({
      showError: 'messages/error',
      showSuccess: 'messages/success'
    }),

    async submit () {
      if (this.newPassword1 !== this.newPassword2) {
        this.showError(this.$t("Password doesn't match"))
        return
      }

      this.showError(null)
      try {
        await this.$axios.post('/change-password', {
          token: this.$route.params.token,
          newPassword: this.newPassword1
        })
        this.showSuccess(this.$t('Password has been updated.'))
      } catch (err) {
        this.handleError(err)
      }
    }
  },

  head () {
    return {
      title: this.$t('Reset Password') + ' – Kairly',
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Reset Password
.reset-password-token-view
  border-radius: 5px
  max-width: 480px
  margin: $baseline auto
  padding: $baseline

  background: #fff
  border: 1px solid #ddd

  //- Heading
  > h1
    margin-bottom: $baseline / 2

    font-size: $fs-2
    font-weight: 600

  > p
    margin-bottom: $baseline

  //- Forms
  form
    > div
      margin-bottom: $baseline

    label
      display: table

      font-weight: 600

    input
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: 250px

      border-radius: 5px 0 0 5px
      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs-0

    button
      +button(primary, medium)
</style>
