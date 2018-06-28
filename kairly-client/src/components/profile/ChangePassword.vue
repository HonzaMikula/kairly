<template>
  <dialog-window :onClose="closeModal">
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

      <button @click="submit">Change Passoword</button>

      <button-close tabindex="0" role="button" @click="closeModal()">Close</button-close>
    </change-password-view>
  </dialog-window>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'ChangePassword',

  props: {
    'onClose': Function
  },

  metaInfo: {
    title: 'Change Password'
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
    closeModal() {
      this.onClose()
    },

    submit() {
      if (this.newPassword1 != this.newPassword2) {
        alert("Password doesn't match")
      } else {
        api.changePassword({
          oldPassword: this.oldPassword,
          newPassword: this.newPassword1
        }).then(() => {
          // even empty hanler must be here to trigger request
          // TODO indicate password changed
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
