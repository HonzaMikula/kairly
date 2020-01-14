<template>
  <AppLayout :name="$t('Account Settings')">
    <div class="settings-view">
      <h1>{{ $t('Account Settings') }}</h1>

      <div>
        <div class="settings--profile-picture">
          <PictureInput
            ref="pictureInput"
            width="104"
            height="104"
            accept="image/jpeg,image/png"
            size="10"
            buttonClass="btn"
            :prefill="user.pictures && user.pictures.big"
            :customStrings="{
              drag: $t('Upload image')
            }"
            @change="onPictureChange"
          />
        </div>

        <div class="settings--form">
          <h2>{{ $t('Personal') }}</h2>
          <div>
            <label for="name">{{ $t('Name') }}</label>
            <input id="name" v-model="name">
          </div>

          <div>
            <label for="medium">{{ $t('Medium') }}</label>
            <input id="medium" v-model="medium">
            <p>{{ $t('Are you writing articles or editing for some medium?') }}</p>
          </div>

          <div>
            <label for="bio">Bio</label>
            <textarea id="bio" v-model="bio" maxlength="280"></textarea>
          </div>

          <div>
            <label for="timezone">{{ $t('Timezone') }}</label>
            <select id="timezone" v-model="timezone">
              <option value="GMT">GMT</option>
              <option value="Europe/Prague">Europe/Prague</option>
            </select>
            <p>{{ $t('Tell us in which timezone are you living in, so we can deliver news at the right time.') }}</p>
          </div>

          <div>
            <h3>{{ $t('Password') }}</h3>
            <p>
              {{ $t('Do you want to have different password?') }}
              <a href="" @click.prevent="isChangePasswordOpen = true">{{ $t('Change password') }}</a>.</p>
          </div>

          <h2>{{ $t('Integrations') }}</h2>

          <div>
            <label for="twitter">{{ $t('Twitter username') }}</label>
            @ <input id="twitter" v-model="twitter">
            <p>{{ $t('Provide us with your Twitter username and we will automatically publish your tweets on Kairly.') }}</p>
          </div>

          <h2>{{ $t('Publishing') }}</h2>

          <div>
            <label for="price">{{ $t('Subscription price') }}</label>
            <select id="price" v-model="price">
              <option value="0">Free</option>
              <option value="25">25 Kč</option>
              <option value="75">75 Kč</option>
              <option value="175">175 Kč</option>
            </select>
            <p>{{ $t('Montly subscription price for my posts.') }}</p>
          </div>

          <button @click="submit">{{ $t('Save profile') }}</button>
        </div>
      </div>

      <ChangePasswordModal
        :active.sync="isChangePasswordOpen"
      />
    </div>
  </AppLayout>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

import PictureInput from '@/lib/vue-picture-input/PictureInput'
import AppLayout from '@/components/layout/AppLayout'
import ChangePasswordModal from '@/components/modals/ChangePasswordModal'
import InfoMessage from '@/components/InfoMessage'

export default {
  name: 'Settings',

  head() {
    return {
      title: this.$t('Account Settings – Kairly')
    }
  },

  components: {
    AppLayout,
    PictureInput,
    ChangePasswordModal,
    InfoMessage
  },

  data() {
    return {
      name: null,
      medium: null,
      bio: null,
      timezone: null,
      twitter: null,
      price: null,
      isChangePasswordOpen: false
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user,
    })
  },

  methods: {
    updateComponentData({ name, medium, bio, timezone, price, integrations: { twitter }}) {
      this.name = name
      this.medium = medium
      this.bio = bio
      this.timezone = timezone
      this.price = ~~price
      this.twitter = twitter
    },

    async updateProfile(payload) {
      const user = await this.$axios.$patch('/profile', payload)
      this.updateComponentData(user)
      // update user in store. Merge properties because GET on /profile endpoint
      // returns more then update (eg owned newspapers)
      this.$auth.setUser({...this.user, ...user})
      this.showSuccess('Your settings were updated.')
    },

    onPictureChange(picture) {
      // Save imediatelly
      this.updateProfile({ picture })
    },

    submit() {
      const { name, medium, bio, timezone, price, twitter } = this
      this.updateProfile({ name, medium, bio, timezone, price, integrations: { twitter }})
    },

    ...mapMutations({
      showError: 'messages/error',
      showSuccess: 'messages/success'
    })
  },

  beforeMount() {
    this.updateComponentData(this.user)
  },

}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'


.settings-view
  position: relative

  display: block
  max-width: 900px
  margin: $baseline auto

  //- Heading
  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

    @media (max-width: $mobile)
      text-align: center

  //- Sections heading
  h2
    margin-bottom: $baseline / 2
    font-size: $fs-2
    font-weight: 600

  //- Wrapper
  > div
    display: grid
    grid-template-columns: $baseline*4  auto
    grid-column-gap: $baseline * 2

    @media (max-width: $mobile)
      display: block
      padding: $baseline / 4


//- Profile Picture
.settings--profile-picture

  //- picture wrapper
  .preview-container
    text-align: center
    &::before
      +fa-icon()
      @extend .fas

      position: absolute
      z-index: 100000
      height: $baseline * 4
      width: $baseline * 4

      background: rgba(0, 0, 0, 0.1)
      border-radius: 100%
      color: rgba(255, 255, 255, 0.7)
      opacity: 0

      font-size: $fs-3
      line-height: $baseline * 4
      text-align: center

      content: fa-content($fa-var-camera)
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
.settings--form

  > div
    dispay: table
    width: $baseline * 14
    margin-bottom: $baseline


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


    //- textarea
    textarea
      box-sizing: border-box
      height: $baseline * 2.5
      padding: $baseline/4
      width: $baseline * 14

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--1

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
      font-size: $fs--1


    //- help
    p
      margin-top: $baseline / 4
      color: #555

      font-size: $fs--1
      line-height: 1.42

      a
        color: darken($c-base, 20%)

        font-weight: 600
        text-decoration: underline

        &:hover,
        &:focus
          text-decoration: none

  //- submit button
  button
    +button

</style>
