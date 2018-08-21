<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" class="change-password" @click.stop>
      <header>
        <h1>Change Password</h1>

        <button-close tabindex="0" role="button" @click="closeModal"></button-close>
      </header>

      <change-password-view role="dialog" @click.stop>
        <div>
          <label for="oldPassword">Old password</label>
          <input id="oldPassword" type="password" v-model="oldPassword">
        </div>

        <div>
          <label for="newPassword">New password</label>
          <input id="newPassword" type="password" v-model="newPassword1">
        </div>

        <div>
          <label for="newPassword2">New password again</label>
          <input id="newPassword2" type="password" v-model="newPassword2">
        </div>
      </change-password-view>

      <footer>
        <button @click="submit">Change password</button>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import * as api from '@/api'

import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'ChangePassword',

  props: {
    closeModal: Function
  },

  head: {
    title: 'Change password - Kairly'
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

  computed: mapGetters(['user']),

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    submit() {
      if (this.newPassword1 != this.newPassword2) {
        this.showError("Password doesn't match")
      } else {
        this.showError(null)
        api.changePassword({
          oldPassword: this.oldPassword,
          newPassword: this.newPassword1
        }).then(() => {
          this.showSuccess("Password has been updated.")
          this.closeModal()
        }, err => {
          if (err.status === 400) {
            this.showError(err.response.data.error)
          } else if (err.status === 401) {
            this.showError('Wrong old password.')
          } else {
            this.showError((err + '') || 'Request failed')
          }
        })
      }
    }
  }
}
</script>

<style lang="sass">
change-password-view
  position: relative

  padding: $baseline
  background: #fff

  //- close button
  button-close
    position: absolute
    top: -$baseline
    right: 0

    text-transform: lowercase
    cursor: pointer

    &::before
      +fa-icon()

      margin-right: $baseline / 4

      content: $fa-var-times

  > div
    dispay: table
    margin-bottom: $baseline

    &:last-of-type
      margin-bottom: 0

    //- label
    label, h3
      display: table

      font-size: $fs--2
      font-weight: 600

    //- input fields
    input
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: $baseline * 8

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--2

  //- submit button
  button
    +subscribe-button

    height: $baseline * 1.25

    border-radius: $baseline*0.75
    background: $c-base
    color: #fff

    font-family: $ff-sans
    font-size: $fs--1

    &:focus,
    &:hover
      background: darken($c-base, 10%)
</style>
