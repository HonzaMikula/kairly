<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="newspaper-subscription-dialog">
      <header>
        <h1 v-if="!subscription.state">{{ $t('Subscribe newspaper') }}</h1>
        <h1 v-else-if="subscription.state === 'active'">{{ $t('Change or cancel subscription') }}</h1>
        <h1 v-else-if="subscription.state === 'canceled'">{{ $t('Renew subscription') }}</h1>
        <h1 v-else-if="subscription.state === 'suspended'">{{ $t('Resolve suspended subscription') }}</h1>

        <button-close tabindex="0" role="button" @keydown.esc="closeModal()" @click="closeModal()"></button-close>
      </header>
      <main>
        <section class="newspaper-subscription--newspaper">
          <h3>{{ newspaper.title }}</h3>
          <picture>
            <img :src="newspaper.picture" :alt="newspaper.title" />
          </picture>
          <time>{{ getPeriodicityLabel(newspaper.periodicity) }}</time>
        </section>

        <section class="newspaper-subscription--price">
          <h2 v-if="!subscription.state">{{ $t('It will cost you') }}</h2>
          <h2 v-else-if="subscription.state === 'active'">{{ $t('It costs you') }}</h2>
          <h2 v-else-if="subscription.state === 'canceled'">{{ $t('You were paying') }}</h2>
          <h2 v-else-if="subscription.state === 'suspended'">{{ $t('You should be paying') }}</h2>

          <p>{{ newspaper.price.split('.')[0] }} {{ $t('Kč per month') }}</p>
        </section>

        <section class="newspaper-subscription--donations">
          <h2>{{ $t('Support the newspaper and donate more') }}</h2>
          <div>
            <input v-model="donation" type="number" :placeholder="$t('Your donation')" min="0" max="100000"/>
            {{ $t('Kč per month') }}
          </div>
        </section>
      </main>
      <footer class="newspaper-subscription--footer">
        <template v-if="!subscription.state">
          <div
            :title="!canPay && $t('You don\'t have enough credit')"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
            <button
              @click="subscribe()"
              :disabled="!canPay"
              class="confirm"
            >
              {{ $t('Subscribe newspaper') }}
            </button>
            <p>{{ $t('* You can cancel subscription any time') }}</p>
          </div>
        </template>

        <template v-else-if="subscription.state === 'active'">
          <button @click="subscribe()" class="confirm">
            {{ $t('Update donation') }}
          </button>

          <button class="cancel" @click="unsubscribe()">
            {{ $t('Cancel subscription') }}
          </button>
        </template>

        <template v-else-if="subscription.state === 'canceled'">
          <button class="confirm" @click="subscribe()">
            {{ $t('Renew subscription') }}
          </button>

          <p>
            {{ $t('You cancled the subscription. It expires on') }}
            <strong>{{ subscription.to|moment('calendar') }}</strong>.
            {{ $t('Till then you will still see the newspaper on the timeline.') }}
          </p>
        </template>

        <template v-else-if="subscription.state === 'suspended'">
          <button class="confirm" v-if="canPay" @click="subscribe()">
            {{ $t('Renew subscription') }}
          </button>
          <nuxt-link v-else to="/user/add-credits">
            {{ $t('Buy credits to renew a subscption') }}
          </nuxt-link>

          <button class="cancel" @click="unsubscribe()">{{ $t('Cancel subscription') }}</button>
        </template>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapState } from 'vuex'

import DialogWindow from '@/components/modals/Dialog'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'

export default {
  name: 'SubscriptionConfirmationDialog',

  props: {
    newspaper: Object,
    subscription: Object,
    closeModal: Function
  },

  components: {
    DialogWindow
  },

  mixins: [PeriodicityMixin],

  data() {
    return {
      donation: this.subscription.donation
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    }),

    canPay() {
      if (this.user) {
        const price = this.newspaper.price.split('.').map(v => ~~v)
        const credits = this.user.credits.split('.').map(v => ~~v)
        return credits[0] > price[0] || (credits[0] == price[0] && credits[1] >= price[1])
      }
      return false
    }
  },

  methods: {
    subscribe() {
      this.$store.dispatch('subscribeNewspaper', {
        fullName: this.newspaper.fullName,
        donation: this.donation ? this.donation : null
      })
      this.closeModal()
    },

    unsubscribe() {
      this.$store.dispatch('unsubscribeNewspaper', {
        fullName: this.newspaper.fullName
      })
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- NEWSPAPER SUBSCRIPTION DIALOG -//
modal-dialog.newspaper-subscription-dialog
  display: block
  max-width: 360px

  main
    padding: $baseline/2 $baseline/2 0 $baseline/2

  //- Author
  .newspaper-subscription--newspaper
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-columns: $baseline*3.5 1fr
    grid-template-rows: auto auto
    grid-template-areas: "newspaper-image newspaper-name" "newspaper-image newspaper-periodicity"

    picture
      grid-area: newspaper-image

      img
        display: block
        height: $baseline * 2
        width: 100%
        object-fit: cover


    h3
      grid-area: newspaper-name

      font-size: $fs-1
      font-weight: 600
      line-height: $baseline * 0.9

    time
      grid-area: newspaper-periodicity

      color: #777

      font-size: $fs--1
      font-weight: 600
      line-height: $baseline * 0.8


  //- Price
  .newspaper-subscription--price
    margin: $baseline/2 0

    text-align: center

    p
      font-size: $fs-1
      font-weight: 600


  //- Donate More
  .newspaper-subscription--donations
    padding: $baseline/2 $baseline/2 $baseline*3/4 $baseline/2
    margin: 0 (-$baseline/2)

    background: #fafafa
    border-top: 1px solid #eee

    > div
      margin-bottom: 0

    //- input field
    input
      border-radius: 5px
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: 160px

      border: 1px solid #eee

      font-family: $ff-sans
      font-size: $fs-0
      font-weight: 600

      &::placeholder
        font-weight: 400

    > div
      font-size: $fs--1

  //- Footer with buttons
  .newspaper-subscription--footer

    //- confirm button
    button.confirm
      +button

    //- cancel button
    button.cancel
      +button
      display: table
      margin: $baseline/2 auto 0 auto

      background: transparent
      border: 0
      color: $c-red

      &:hover,
      &:focus
        background: $c-red
        color: #fff

    //- foot note
    button + p
      margin-top: $baseline / 4

      font-size: $fs--1
      line-height: $baseline * 0.8

    a
      color: $c-base
</style>
