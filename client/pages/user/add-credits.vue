<template>
  <app-layout :name="$t('Add Credit')">
    <div class="buy-credits-view">
      <h1>{{ $t('Buy Credits') }}</h1>

      <p>
        {{ $t('Kairly is currently in beta. You will receive free credit automatically every month.') }}
      </p>

      <p>
        {{ $t('In future you will have to buy credit. But we will also start paying authors and editors for their good work.') }}
      </p>

      <p style="margin-top: 20px">
        {{ $t('Do you need more credits?') }}
        <br>

        <button :disabled="btnDisabled" @click="requestCredits">{{ $t('Please, give me more') }}</button>
      </p>
    </div>
  </app-layout>
</template>

<script>
import { mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'


export default {
  name: 'AddCredit',

  head() {
    return {
      title: this.$t('Add Credit – Kairly')
    }
  },

  data() {
    return {
      btnDisabled: false
    }
  },

  computed: mapState({
    user: state => state.auth.user,
  }),

  components: {
    AppLayout,
  },

  methods: {
    async requestCredits() {
      this.btnDisabled = true
      if (this.user.credits < 2500) {
        const { credits } = await this.$axios.$post('/buy-credits')
        this.$store.commit('updateCredits', credits)
        this.timer = setTimeout(() => {
          this.btnDisabled = false
          this.timer = null
        }, 3000)
      } else {
        alert(this.$t("Don't be greedy."))
      }
    }
  },

  beforeDestroy() {
    if (this.timer) {
      clearTimeout(this.timer)
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- BUY CREDITS VIEW -//
.buy-credits-view
  max-width: 900px
  margin: 0 auto
  padding: $baseline 0

  //- Heading
  > h1
    margin-bottom: $baseline

    font-weight: 600
    font-size: $fs-3

  button
    +button
    margin-top: 10px

</style>
