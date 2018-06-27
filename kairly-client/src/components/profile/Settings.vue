<template>
  <app-layout>
    <settings-view>
      <h1>Account Setting</h1>

      <settings--change-password>
        <router-link :to="{name: 'change-password'}">Change password</router-link>
      </settings--change-password>

      <div>
        <settings--profile-picture>
          <picture-input
            ref="pictureInput"
            @change="onPictureChange"
            width="104"
            height="104"
            accept="image/jpeg,image/png"
            size="10"
            buttonClass="btn"
            :prefill="this.user.picture"
            :customStrings="{
              drag: 'Drag or upload image'
            }">
          </picture-input>
        </settings--profile-picture>

        <settings--form>
          <h2>Personal</h2>
          <div>
            <label for="name">Name</label>
            <input id="name" v-model="name">
          </div>

          <div>
            <label for="medium">Medium</label>
            <input id="medium" v-model="medium">
            <p>Are you writing articles or editing for some medium?</p>
          </div>

          <div>
            <label for="bio">Bio</label>
            <textarea id="bio" v-model="bio"></textarea>
          </div>

          <div>
            <label for="timezone">Timezone</label>
            <select id="timezone" v-model="timezone">
              <option value="GMT">GMT</option>
              <option value="Europe/Prague">Europe/Prague</option>
            </select>
            <p>Tell us in which timezone are you living, so we can deliver news at right time.</p>
          </div>

          <h2>Integrations</h2>

          <div>
            <label for="twitter">Twitter Username</label>
            @ <input id="twitter" v-model="twitter">
            <p>Provide us with your Twitter username and we will automatically publish your tweets on Kairly.</p>
          </div>


          <button @click="submit">Save profile</button>
        </settings--form>
      </div>
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
  position: relative

  display: block
  max-width: 900px
  margin: $baseline auto

  //- Heading
  h1
    margin-bottom: $baseline

    font-size: $fs-2
    font-weight: 600

    @media (max-width: $mobile)
      text-align: center

  //- Sections heading
  h2
    margin-bottom: $baseline / 2
    font-size: $fs-1
    font-weight: 600

  //- Wrapper
  > div
    display: grid
    grid-template-columns: $baseline*4  auto
    grid-column-gap: $baseline * 2

    @media (max-width: $mobile)
      display: block
      padding: $baseline / 4

//- Change Password
settings--change-password
  position: absolute
  right: 0
  top: 0

  @media (max-width: $mobile)
    position: static

    display: block
    margin-bottom: $baseline / 2

    text-align: center

  a
    +subscribe-button

    display: inline-block
    border-radius: $baseline*0.75

    font-family: $ff-sans
    font-size: $fs--1
    line-height: $baseline * 1.25


//- Profile Picture
settings--profile-picture

  //- picture wrapper
  .preview-container
    &::before
      +fa-icon()

      position: absolute
      z-index: 100000
      height: $baseline * 4
      width: $baseline * 4

      background: rgba(0, 0, 0, 0.1)
      border-radius: 100%
      color: rgba(255, 255, 255, 0.7)
      opacity: 0

      font-size: $fs-2
      line-height: $baseline * 4
      text-align: center

      content: $fa-var-camera
      pointer-events: none
      transition: 0.15s opacity

    &:hover::before
      opacity: 1

  //- picture
  canvas
    border-radius: 100% !important

  //- change picture button
  button
    background: transparent
    border: 0
    color: #555

    &:focus,
    &:hover
      color: #000

//- Form Section
settings--form

  > div
    dispay: table
    width: $baseline * 14
    margin-bottom: $baseline


    //- label
    label
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


    //- textarea
    textarea
      box-sizing: border-box
      height: $baseline * 2.5
      width: $baseline * 14

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--2

      @media (max-width: $mobile)
        width: 100%


    //- select
    select
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: $baseline * 8

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--2


    //- help
    p
      margin-top: $baseline / 4
      color: #555

      font-size: $fs--3
      line-height: $baseline * 0.7

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
