<template>
  <AppLayout>
    <main class="reset-password-view">
      <h1>{{ $t('Reset password') }}</h1>
      <ol>
        <li>{{ $t('Enter your email.') }}</li>
        <li>{{ $t('We will send you email with link.') }}</li>
        <li>{{ $t('Open the link and set your new password.') }}</li>
      </ol>
      <template v-if="step === 'form'">
        <form
          v-if="step === 'form'"
          @submit.prevent="submit"
        >
          <label for="email">{{ $t('Your email') }}</label>
          <div>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="@"
            >
            <button type="submit">{{ $t('Request reset') }}</button>
          </div>
        </form>
      </template>
      <div v-else class="reset-password--message">
        <h3>{{ $t('Password reset requested') }}</h3>
        <p>{{ $t('Check your inbox for email with the reset link.') }}</p>
      </div>
    </main>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'ResetPassword',

  auth: false,

  components: {
    AppLayout,
  },

  mixins: [ErrorHandler],

  data () {
    return {
      step: 'form',
      email: '',
    }
  },

  methods: {
    async submit () {
      try {
        await this.$axios.post('/reset-password', {
          email: this.email
        })
        this.step = 'submit'
      } catch (err) {
        this.handleError(err)
      }
    }
  },

  head () {
    return {
      title: this.$t('Reset password') + ' – Kairly',
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Reset Password
.reset-password-view
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

  //- Tips
  ol
    margin-bottom: $baseline
  ol li
    list-style: decimal inside

  //- Form
  form

    label
      display: table
      font-weight: 600

    > div
      display: flex

    input
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: 250px

      border-radius: 5px 0 0 5px
      border: 1px solid #ddd
      border-right: 0

      font-family: $ff-sans
      font-size: $fs-0

    button
      +button(primary, medium)

      border-radius: 0 5px 5px 0

//- Message
.reset-password--message
  background: lighten($c-base, 30%)
  border: 1px solid $c-base
  padding: $baseline / 2

  h3
    margin-bottom: $baseline / 4

    font-weight: 600

  p
    font-size: $fs--1

</style>
