<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="author-subscription-dialog">
      <header>
        <h1 v-if="!subscription.state">{{ $t('Subscribe to author') }}</h1>
        <h1 v-else-if="subscription.state === 'active'">{{ $t('Change or cancel subscription') }}</h1>
        <h1 v-else-if="subscription.state === 'canceled'">{{ $t('Renew subscription') }}</h1>
        <h1 v-else-if="subscription.state === 'suspended'">{{ $t('Resolve suspended subscription') }}</h1>

        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <main>
        <section class="author-subscription--author">
          <h3>{{ author.name }}</h3>
          <img :src="author.picture" />
          <time>{{ getPeriodicityLabel(periodicity) }}</time>
          <a href="" @click.prevent="showChangePeriodicityDialog = !showChangePeriodicityDialog">{{ $t('change periodicity') }}</a>
        </section>

        <transition name="change-periodicity-animation">
          <ChangePeriodicity
            v-if="showChangePeriodicityDialog"
            :author="author"
            :subscription="subscription"
            @changePeriodicity="changePeriodicity"
          />
        </transition>

        <section class="author-subscription--price">
          <h2 v-if="!subscription.state">{{ $t('It will cost you') }}</h2>
          <h2 v-else-if="subscription.state === 'active'">{{ $t('It costs you') }}</h2>
          <h2 v-else-if="subscription.state === 'canceled'">{{ $t('You were paying') }}</h2>
          <h2 v-else-if="subscription.state === 'suspended'">{{ $t('You should be paying') }}</h2>

          <p>{{ author.price.split('.')[0] }} {{ $t('Kč per month') }}</p>
        </section>

        <section class="author-subscription--donations">
          <h2>{{ $t('To support exceptional journalist, donate more') }}</h2>
          <div>
            <input v-model="donation" type="number" :placeholder="$t('Your donation')" min="0"/>
            {{ $t('Kč per month') }}
          </div>
        </section>
      </main>
      <footer class="author-subscription--footer">
        <template v-if="!subscription.state">
          <div
            :title="!canPay && $t('You don\'t have enough credit')"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
            <button
              class="confirm"
              @click="subscribe()"
              :disabled="!canPay"
            >
              {{ $t('Subscribe') }}
            </button>

            <p>{{ $t('* You can cancel subscription any time') }}</p>
          </div>
        </template>

        <template v-else-if="subscription.state === 'active'">
          <button class="confirm" @click="subscribe()">{{ $t('Update donation') }}</button>

          <button class="cancel" @click="unsubscribe()">{{ $t('Cancel subscription') }}</button>
        </template>

        <template v-else-if="subscription.state === 'canceled'">
          <button class="confirm" @click="subscribe()">
            {{ $t('Renew subscription') }}
          </button>
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
import ChangePeriodicity from '@/components/widgets/ChangePeriodicity'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'

export default {
  name: 'AuthorSubscriptionConfirmationDialog',

  props: {
    author: Object,
    subscription: Object,
    closeModal: Function
  },

  components: {
    DialogWindow,
    ChangePeriodicity
  },

  mixins: [PeriodicityMixin],

  data() {
    return {
      donation: this.subscription.donation,
      periodicity: this.subscription.periodicity || {frequency: '6x_per_day'},
      showChangePeriodicityDialog: false
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    }),

    periodicityLabel() {
      return this.getPeriodicityLabel(this.periodicity)
    },

    canPay() {
      if (this.user) {
        const price = this.author.price.split('.').map(v => ~~v)
        const credits = this.user.credits.split('.').map(v => ~~v)
        return credits[0] > price[0] || (credits[0] == price[0] && credits[1] >= price[1])
      }
      return false
    }
  },

  methods: {
    changePeriodicity(frequency, dow, time) {
      this.showChangePeriodicityDialog = false

      this.periodicity = {
        "frequency": frequency,
        "dow": dow,
        "time": time
      }
    },

    subscribe() {
      this.$store.dispatch('subscribeAuthor', {
        author: this.author,
        periodicity: this.periodicity,
        donation: this.donation ? this.donation : null
      })
      this.closeModal()
    },

    unsubscribe() {
      this.$store.dispatch('unsubscribeAuthor', {
        author: this.author,
      })
      this.closeModal()
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- AUTHOR SUBSCRIPTION DIALOG -//
modal-dialog.author-subscription-dialog
  display: block

  main
    padding: $baseline/2 $baseline/2 0 $baseline/2

  //- Author
  .author-subscription--author
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-columns: $baseline*2 1fr auto
    grid-template-rows: $baseline*1.2 $baseline*0.8
    grid-template-areas: "author-image author-name ." "author-image author-periodicity author-change"

    img
      grid-area: author-image
      border-radius: 100%
      height: $baseline * 2
      width: $baseline * 2

    h3
      grid-area: author-name
      font-size: $fs-1
      font-weight: 600
      line-height: $baseline * 1.2

    time
      grid-area: author-periodicity

      color: #777

      font-size: $fs--1
      font-weight: 600
      line-height: $baseline * 0.8

    a
      grid-area: author-change

      color: $c-base

      font-size: $fs--1
      line-height: $baseline * 0.8

  //- Price
  .author-subscription--price
    margin: $baseline/2 0

    text-align: center

    p
      font-size: $fs-1
      font-weight: 600

  //- Change Periodicity Dialog

  .change-periodicity-view
    position: absolute
    right: $baseline / 2
    width: 280px


  //- Donate More
  .author-subscription--donations
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
  .author-subscription--footer

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
      font-size: $fs--1

    a
      color: $c-base
</style>
