<template>
  <app-layout>
    <settings-view>
      <main>
        <h2>Personal Info</h2>

        PICTURE INPUT HERE

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

        <a href="#">Change password</a>

        <h2>Twitter</h2>

        <input placeholder="Twitter account" v-model="twitter">

        <br/>

        <button @click="submit">Save profile</button>
      </main>
    </settings-view>
  </app-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'Settings',

  components: {
    AppLayout
  },

  data() {
    return {
      name: null,
      medium: null,
      bio: null,
      timezone: null,
      twitter: null
      //picture = models.ImageField(upload_to='users', null=True)  # temporary allow null

    }
  },

  computed: mapGetters(['user']),

  methods: {
    updateFrom({ name, medium, bio, timezone }) {
      this.name = name
      this.medium = medium
      this.bio = bio
      this.timezone = timezone
    },

    submit() {
      const { name, medium, bio, timezone } = this
      // empty .then needed to trigger request
      api.updateProfile({ name, medium, bio, timezone })
      .then(res => {
        this.updateFrom(res.body)
        // TODO update store, use action
      })
    }
  },

  beforeMount() {
    this.updateFrom(this.user)
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
