<template>
  <app-layout>
    <settings-view>
      <main>
        <h2>Personal Info</h2>

        <picture-input
          ref="pictureInput"
          @change="onPictureChange"
          width="200"
          height="200"
          margin="16"
          accept="image/jpeg,image/png"
          size="10"
          buttonClass="btn"
          :prefill="this.user.picture"
          :customStrings="{
            drag: 'Drag or upload image'
          }">
        </picture-input>

        <div>
          <input placeholder="Name" v-model="name">
        </div>
        <div>
          <input placeholder="Medium" v-model="medium">
        </div>
        <div>
          <textarea placeholder="Bio" v-model="bio"></textarea>
        </div>
        <div>
          <select placeholder="Timezone" v-model="timezone">
            <option value="GMT">GMT</option>
            <option value="Europe/Prague">Europe/Prague</option>
          </select>
        </div>

        <router-link :to="{name: 'change-password'}">Change password</router-link>

        <h2>Twitter</h2>

        <input placeholder="Twitter account" v-model="twitter">

        <br/>

        <button @click="submit">Save profile</button>
      </main>
    </settings-view>
  </app-layout>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import * as api from '@/api'

import PictureInput from 'vue-picture-input'
import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'Settings',

  components: {
    AppLayout,
    PictureInput
  },

  data() {
    return {
      name: null,
      medium: null,
      bio: null,
      timezone: null,
      twitter: null
    }
  },

  computed: mapGetters(['user']),

  methods: {
    updateComponentData({ name, medium, bio, timezone }) {
      this.name = name
      this.medium = medium
      this.bio = bio
      this.timezone = timezone
    },

    updateProfile(payload) {
      api.updateProfile(payload)
      .then(res => {
        const user = res.body
        this.updateComponentData(user)
        this.updateUserInStore(user)
      })
    },

    onPictureChange(picture) {
      // Save imediatelly
      this.updateProfile({ picture })
    },

    submit() {
      const { name, medium, bio, timezone } = this
      this.updateProfile({ name, medium, bio, timezone })
    },

    ...mapMutations({updateUserInStore: 'user'})
  },

  beforeMount() {
    this.updateComponentData(this.user)
  }


}
</script>

<style lang="sass">
settings-view
  main
    max-width: 970px
    margin: $baseline auto

  h2
    font-size: 24rem
    font-weight: bold
    margin: 20px 0

</style>
