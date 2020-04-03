<template>
  <DialogWindow
    v-if="active"
    custom-class="author-subscription-dialog"
    @close="closeModal"
  >
    <template #header>
      <h1 v-if="!state">{{ $t('Subscribe to author') }}</h1>
      <h1 v-else-if="state === 'active'">{{ $t('Change or cancel subscription') }}</h1>
      <h1 v-else-if="state === 'canceled'">{{ $t('Renew subscription') }}</h1>
      <h1 v-else-if="state === 'suspended'">{{ $t('Resolve suspended subscription') }}</h1>
    </template>

    <section class="author-subscription--author">
      <h3>{{ author.name }}</h3>
      <picture>
        <AuthorPicture :author="author" />
      </picture>

      <time>{{ getPeriodicityLabel(periodicity) }}</time>
      <a href="" @click.prevent.stop="showChangePeriodicityDialog = !showChangePeriodicityDialog">{{ $t('change periodicity') }}</a>
    </section>

    <ChangePeriodicity
      v-if="showChangePeriodicityDialog"
      @changePeriodicity="changePeriodicity"
    />

    <section class="author-subscription--price">
      <h2 v-if="!state">{{ $t('It will cost you') }}</h2>
      <h2 v-else-if="state === 'active'">{{ $t('It costs you') }}</h2>
      <h2 v-else-if="state === 'canceled'">{{ $t('You were paying') }}</h2>
      <h2 v-else-if="state === 'suspended'">{{ $t('You should be paying') }}</h2>

      <p>
        <MoneyFormat :value="author.price" :short="true" />
        {{ $t('Kč per month') }}
      </p>
    </section>

    <section class="author-subscription--donations">
      <h2>{{ $t('Support the author and donate more') }}</h2>
      <div>
        <input v-model="donation" type="number" :placeholder="$t('Your donation')" min="0" max="100000">
        {{ $t('Kč per month') }}
      </div>
    </section>

    <template #footer>
      <template v-if="!state">
        <div
          v-b-tooltip
          :title="!canPay && $t('You don\'t have enough credit')"
        >
          <button
            class="confirm"
            :disabled="!canPay"
            @click="subscribe()"
          >
            {{ $t('Subscribe') }}
          </button>

          <p>{{ $t('* You can cancel subscription any time') }}</p>
        </div>
      </template>

      <template v-else-if="state === 'active'">
        <button
          class="confirm"
          @click="subscribe()"
        >
          {{ $t('Update subscription') }}
        </button>

        <button
          class="cancel"
          @click="unsubscribe()"
        >
          {{ $t('Cancel subscription') }}
        </button>
      </template>

      <template v-else-if="state === 'canceled'">
        <button
          class="confirm"
          @click="subscribe()"
        >
          {{ $t('Renew subscription') }}
        </button>

        <p>
          {{ $t('You cancled the subscription. It expires on') }}
          <strong>{{ subscription.to|moment('calendar') }}</strong>.
          {{ $t('Till then you will still see the author on the timeline.') }}
        </p>
      </template>

      <template v-else-if="state === 'suspended'">
        <button
          v-if="canPay"
          class="confirm"
          @click="subscribe()"
        >
          {{ $t('Renew subscription') }}
        </button>

        <nuxt-link v-else to="/user/add-credits">
          {{ $t('Buy credits to renew a subscption') }}
        </nuxt-link>

        <button class="cancel" @click="unsubscribe()">{{ $t('Cancel subscription') }}</button>
      </template>
    </template>
  </DialogWindow>
</template>

<script>
import { mapState } from 'vuex'

import AuthorPicture from '@/components/widgets/AuthorPicture'
import DialogWindow from '@/components/modals/DialogWindow'
import ChangePeriodicity from '@/components/widgets/ChangePeriodicity'
import ModalMixin from '@/mixins/ModalMixin'
import MoneyFormat from '@/components/widgets/MoneyFormat'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'

export default {
  name: 'AuthorSubscriptionModal',

  components: {
    AuthorPicture,
    DialogWindow,
    ChangePeriodicity,
    MoneyFormat,
  },

  mixins: [ModalMixin, PeriodicityMixin],

  props: {
    author: Object,
  },

  data () {
    const subscription = this.$store.getters.getAuthorSubscription(this.author)
    return {
      subscription,
      donation: subscription ? parseInt(subscription.donation) : 0,
      periodicity: (subscription && subscription.periodicity) || { frequency: '6x_per_day' },
      showChangePeriodicityDialog: false
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    }),

    state () {
      return this.subscription ? this.subscription.state : null
    },

    periodicityLabel () {
      return this.getPeriodicityLabel(this.periodicity)
    },

    canPay () {
      if (this.user) {
        const price = this.author.price.split('.').map(v => ~~v)
        const credits = this.user.credits.split('.').map(v => ~~v)
        return credits[0] > price[0] || (credits[0] === price[0] && credits[1] >= price[1])
      }
      return false
    }
  },

  methods: {
    changePeriodicity (frequency, dow, time) {
      this.showChangePeriodicityDialog = false

      this.periodicity = {
        frequency,
        dow,
        time
      }
    },

    closeChangePeriodicityDialog () {
      this.showChangePeriodicityDialog = false
    },

    subscribe () {
      this.$store.dispatch('subscribeAuthor', {
        author: this.author,
        periodicity: this.periodicity,
        donation: this.donation ? this.donation : null
      })
      this.closeModal()
    },

    async unsubscribe () {
      this.subscription = await this.$store.dispatch('unsubscribeAuthor', {
        author: this.author,
      })
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- AUTHOR SUBSCRIPTION DIALOG -//
.modal-dialog.author-subscription-dialog
  display: block
  max-width: 360px

  main
    padding: $baseline/2 $baseline/2 0 $baseline/2

  //- Author
  .author-subscription--author
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-columns: $baseline*2 1fr auto
    grid-template-rows: auto auto
    grid-template-areas: "author-image author-name author-name" "author-image author-periodicity author-change"

    picture
      grid-area: author-image

    img
      border-radius: 100%
      height: $baseline * 2
      width: $baseline * 2

    h3
      grid-area: author-name
      font-size: $fs-1
      font-weight: 600
      line-height: $baseline * 0.9

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
  footer

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
      box-shadow: none
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
