<template>
  <AppLayout>
    <template v-if="step === 'form'">
      <form @submit.prevent="submit">
        Enter your email
        <input
          type="email"
          v-model="email"
        />
        <button type="submit">Request reset</button>
      </form>
    </template>
    <template v-else>
      Check your email.
    </template>
  </AppLayout>
</template>

<script>
import { mapMutations } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'ResetPassword',

  auth: false,

  components: {
    AppLayout,
  },

  head() {
    return {
      title: this.$t('Reset Password') +' – Kairly',
    }
  },

  data() {
    return {
      'step': 'form',
      'email': '',
    }
  },

  methods: {
    ...mapMutations(['showError']),

    async submit() {
      try {
        const res = await this.$axios.post('/reset-password', {
          email: this.email
        })
        this.step = 'submit'
      } catch (err) {
        if (err.response.status === 400) {
          this.showError(err.response.data.error)
        } else {
          this.showError((err + '') || 'Request failed')
        }
      }
    }
  }
}
</script>

<style lang="sass">
</style>
