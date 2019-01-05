<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="subscription-confirmation">
      <header>
        <h1 v-if="!subscription.state">Subscribe newspaper</h1>
        <h1 v-else-if="subscription.state === 'active'">Change or cancel subscription</h1>
        <h1 v-else-if="subscription.state === 'canceled'">Renew subscription</h1>
        <h1 v-else-if="subscription.state === 'suspended'">Resolve suspended subscription</h1>

        <button-close tabindex="0" role="button" @keydown.esc="closeModal()" @click="closeModal()"></button-close>
      </header>
      <main>
        <section v-if="!subscription.state">
          <div>
            <h2>You want to subscribe to</h2>
            <p>{{ newspaper.title }}</p>
            <time>{{ periodicity }}</time>
          </div>

          <div>
            <h2>It will cost you</h2>
            <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
            <p>* You can cancel subscription any time</p>
          </div>
        </section>

        <section v-else-if="subscription.state === 'active'">
          <div>
            <h2>You are subscribed to</h2>
            <p>{{ newspaper.title }}</p>
            <time>{{ periodicity }}</time>
          </div>

          <div>
            <h2>It costs you</h2>
            <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
            <p>* You can cancel subscription any time</p>
          </div>
        </section>

        <section v-else-if="subscription.state === 'canceled'">
          <div>
            <h2>You canceled subscription to</h2>
            <p>{{ newspaper.title }}</p>
            <time>{{ periodicity }}</time>
          </div>

          <div>
            <h2>You were paying</h2>
            <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
          </div>
        </section>

        <section v-else-if="subscription.state === 'suspended'">
          <div>
            <h2>Your subscription were suspended due to not having enough credits.</h2>
            <p>{{ newspaper.title }}</p>
            <time>{{ periodicity }}</time>
          </div>

          <div>
            <h2>You were paying</h2>
            <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
          </div>
        </section>

        <section class="donate-more">
          <h2>To support exceptional journalist, donate more</h2>
          <div>
            <input v-model="donation" type="number" placeholder="Your donation" min="0"/>
            Kč per month
          </div>
        </section>
      </main>
      <footer class="subscription-confirmation--footer">
        <template v-if="!subscription.state">
          <button @click="subscribe()">Subscribe newspaper</button>
        </template>

        <template v-else-if="subscription.state === 'active'">
          <button @click="subscribe()">Update donation</button>

          <button class="cancel" @click="unsubscribe()">Cancel subscription</button>
        </template>

        <template v-else-if="subscription.state === 'canceled'">
          <button @click="subscribe()">
            Renew subscription
          </button>
        </template>

        <template v-else-if="subscription.state === 'suspended'">
          <button v-if="canPay" @click="subscribe()">
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

    periodicity() {
      return this.getPeriodicityLabel(this.newspaper.periodicity)
    },

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
modal-dialog.subscription-confirmation
  display: block

  main
    padding: $baseline/2 $baseline 0 $baseline
    text-align: left

    > section

      > div
        margin-bottom: $baseline

      //- what is it about
      h2
      margin-bottom: $baseline / 4

      //- bold text
      h2 + p
        font-size: $fs-1
        font-weight: 600

      //- periodicity
      time
        color: #777

        font-size: $fs--1
        font-weight: 600
        line-height: $baseline * 0.8

      //- note
      h2 + p + p
        font-size: $fs--1
        margin-bottom: $baseline / 2


    //- Donate More
    .donate-more
      padding: $baseline/2 $baseline $baseline*3/4 $baseline
      margin: 0 (-$baseline)

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

      //- currency
      span
        position: absolute

        line-height: $baseline * 1.25

      > div
        font-size: $fs--1

  //- Footer with buttons
  > footer

    //- confirm button
    button.confirm
      +subscribed-button

      height: $baseline * 1.25

      font-size: $fs-0
      line-height: $baseline * 1.25

    button.cancel
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
      font-size: $fs--1
</style>
