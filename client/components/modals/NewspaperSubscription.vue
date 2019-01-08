<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="newspaper-subscription-dialog">
      <header>
        <h1 v-if="!subscription.state">Subscribe newspaper</h1>
        <h1 v-else-if="subscription.state === 'active'">Change or cancel subscription</h1>
        <h1 v-else-if="subscription.state === 'canceled'">Renew subscription</h1>
        <h1 v-else-if="subscription.state === 'suspended'">Resolve suspended subscription</h1>

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
          <h2 v-if="!subscription.state">It will cost you</h2>
          <h2 v-else-if="subscription.state === 'active'">It costs you</h2>
          <h2 v-else-if="subscription.state === 'canceled'">You were paying</h2>
          <h2 v-else-if="subscription.state === 'suspended'">You should be paying</h2>

          <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
        </section>

        <section class="newspaper-subscription--donations">
          <h2>To support exceptional journalist, donate more</h2>
          <div>
            <input v-model="donation" type="number" placeholder="Your donation" min="0"/>
            Kč per month
          </div>
        </section>
      </main>
      <footer class="newspaper-subscription--footer">
        <template v-if="!subscription.state">
          <div
            :title="!canPay && 'You don\'t have enough credit'"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
            <button
              @click="subscribe()"
              :disabled="!canPay"
              class="confirm"
            >
              Subscribe newspaper
            </button>
            <p>* You can cancel subscription any time</p>
          </div>
        </template>

        <template v-else-if="subscription.state === 'active'">
          <button @click="subscribe()" class="confirm">Update donation</button>

          <button class="cancel" @click="unsubscribe()">Cancel subscription</button>
        </template>

        <template v-else-if="subscription.state === 'canceled'">
          <button class="confirm" @click="subscribe()">
            Renew subscription
          </button>
        </template>

        <template v-else-if="subscription.state === 'suspended'">
          <button class="confirm" v-if="canPay" @click="subscribe()">
            Renew subscription
          </button>
          <nuxt-link v-else to="/user/add-credits">
            Buy credits to renew a subscption.
          </nuxt-link>

          <button class="cancel" @click="unsubscribe()">Cancel subscription</button>
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
      this.closeModal()
    }
  }
}
</script>

<style lang="sass">
modal-dialog.newspaper-subscription-dialog
  display: block

  main
    padding: $baseline/2 $baseline/2 0 $baseline/2

  //- Author
  .newspaper-subscription--newspaper
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-columns: $baseline*3.5 1fr
    grid-template-rows: $baseline*1.2 $baseline*0.8
    grid-template-areas: "newspaper-image newspaper-name" "newspaper-image newspaper-periodicity"

    picture
      grid-area: newspaper-image

      img
        height: 100%
        width: 100%
        object-fit: cover


    h3
      grid-area: newspaper-name
      font-size: $fs-1
      font-weight: 600
      line-height: $baseline * 1.2

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
    padding: $baseline/2 $baseline $baseline*3/4 $baseline
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
      +subscribed-button

      height: $baseline * 1.25
      padding: 0 $baseline

      font-size: $fs-0
      line-height: $baseline * 1.25

    button.cancel
      display: table
      border-radius: 5px
      margin: $baseline/2 auto 0 auto
      padding: 0 $baseline

      background: transparent
      border: 0
      color: $c-red

      &:hover,
      &:focus
        background: $c-red
        color: #fff

    //- foot note
    button + p
      font-size: $fs--1

    a
      color: $c-base
</style>
