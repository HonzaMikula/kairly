<template>
  <AppLayout>
    <div class="signup-page">
      <SignUpForm />

      <section class="signup-why">
        <ul>
          <li>{{ $t('No notifications. No endless scrolling. No addiction and FOMO.') }}</li>
          <li>{{ $t('Read your sources at regular time you want. E.g. every day at 9am.') }}</li>
          <li>{{ $t('We update your timeline only every 3 hours. Because that\'s sane.') }}</li>
          <li>{{ $t('No magic algorithms. The content is chosen by you and the professional editors you trust.') }}</li>
        </ul>
      </section>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import SignUpForm from '@/components/microsite/SignUpForm'

export default {
  name: 'SignUp',

  auth: false,

  components: {
    AppLayout,
    SignUpForm
  },

  head () {
    return {
      title: this.$t('Sign Up') + ' – Kairly',
      meta: [
        { hid: 'description', name: 'description', content: this.$t('Kairly is platform which aims to improve environment for journalism. Sign up for beta version.') },
      ]
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- SIGN UP PAGE -//
.signup-page
  max-width: 500px
  margin: $baseline auto

  display: grid
  grid-template-columns: auto
  grid-row-gap: $baseline

.signup-why
  align-self: center

  > h2
    margin-bottom: $baseline / 2

    font-size: $fs-3
    font-weight: 600

  ul
    padding: 0 $baseline 0 0

    counter-reset: benefits

    @media (max-width: $mobile)
      padding: 0 $baseline/2

  li
    display: flex
    align-items: center
    margin-bottom: $baseline

    font-size: $fs-1
    line-height: 1.42

    &:last-of-type
      margin-bottom: 0

    @media (max-width: $mobile)
      font-size: $fs-0
      line-height: 1.42

    &::before
      display: inline-block
      margin-right: $baseline / 2
      border-radius: 100%
      height: $baseline * 1.25
      width: $baseline * 1.25
      flex: 0 0 $baseline * 1.25

      background: #fff

      font-size: $fs-0
      font-weight: 600
      line-height: $baseline * 1.25
      text-align: center

      counter-increment: benefits
      content: counter(benefits)

</style>
