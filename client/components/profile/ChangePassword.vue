<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" class="change-password-dialog" @click.stop>
      <header>
        <h1>{{ $t('Change Password') }}</h1>

        <button-close tabindex="0" role="button" @click="closeModal"></button-close>
      </header>

      <change-password-view role="dialog" @click.stop>
        <div>
          <label for="oldPassword">{{ $t('Old password') }}</label>
          <input id="oldPassword" type="password" v-model="oldPassword">
        </div>

        <div>
          <label for="newPassword">{{ $t('New password') }}</label>
          <input id="newPassword" type="password" v-model="newPassword1">
        </div>

        <div>
          <label for="newPassword2">{{ $t('New password again') }}</label>
          <input id="newPassword2" type="password" v-model="newPassword2">
        </div>
      </change-password-view>

      <footer>
        <button @click="submit">{{ $t('Change password') }}</button>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapMutations } from 'vuex'


import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'ChangePassword',

  props: {
    closeModal: Function
  },

  head() {
    return {
      title: this.$t('Change password - Kairly')
    }
  },

  components: {
    DialogWindow
  },

  data() {
    return {
      oldPassword: '',
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
          oldPassword: this.oldPassword,
          newPassword: this.newPassword1
        })
        this.showSuccess(this.$t("Password has been updated."))
        this.closeModal()
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
//- Imports
@import './styles/components/buttons'

//- CHANGE PASSWORD VIEW -//
.change-password-dialog
  header
    h1
      padding: 0 $baseline


change-password-view
  position: relative

  padding: $baseline
  background: #fff

  > div
    dispay: table
    margin-bottom: $baseline

    &:last-of-type
      margin-bottom: 0

    //- label
    label, h3
      display: table

      font-size: $fs--1
      font-weight: 600

    //- input fields
    input
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: $baseline * 8

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--1
</style>
