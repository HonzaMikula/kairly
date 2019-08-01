<template>
  <AppLayout>
    <form
      @submit.prevent="submit"
    >
      <div>
        <label for="newPassword">{{ $t('New password') }}</label>
        <input
          id="newPassword"
          v-model="newPassword1"
          type="password"
        />
      </div>

      <div>
        <label for="newPassword2">{{ $t('New password again') }}</label>
        <input
          id="newPassword2"
          v-model="newPassword2"
          type="password"
        />
      </div>


      <button type="submit">{{ $t('Change password') }}</button>
    </form>
  </AppLayout>
</template>

<script>
import { mapMutations } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'ResetPasswordForm',

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
      newPassword1: '',
      newPassword2: ''
    }
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    async submit() {
      if (this.newPassword1 != this.newPassword2) {
        this.showError(this.$t("Password doesn't match"))
        return
      }

      this.showError(null)
      try {
        const res = await this.$axios.post('/change-password', {
          token: this.$route.params.token,
          newPassword: this.newPassword1
        })
        this.showSuccess(this.$t("Password has been updated."))
      } catch (err) {
        if (err.response && err.response.status === 400) {
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
