<template>
  <app-layout>
    <chnage-password-view>
      <main>

        <div>
          <input placeholder="Old Password" type="password" v-model="oldPassword">
        </div>

        <div>
          <input placeholder="New Password" type="password" v-model="newPassword1">
        </div>

        <div>
          <input placeholder="New Password" type="password" v-model="newPassword2">
        </div>

        <button @click="submit">Change Passoword</button>
      </main>
    </chnage-password-view>
  </app-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

import PictureInput from 'vue-picture-input'
import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'Settings',

  components: {
    AppLayout
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
chnage-password-view
  main
    max-width: 970px
    margin: $baseline auto
</style>
