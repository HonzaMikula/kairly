<template>
  <button
    class="newspaper-subscription-button"
    :class="{
      'to-subscribe': !subscription,
      'is-subscribed': state === 'active',
      'is-canceled': state === 'canceled',
      'is-suspended': state === 'suspended',
    }"
    v-b-tooltip
    :title="buttonTitle"
    @click="(ev) => $emit('click', ev)"
  >
    <template v-if="!subscription || state === 'canceled'">
      {{ price === 0 ? $t('Subscribe for free') : $t('Subscribe for {price}', { price: priceWithCurrency }) }}
      <template v-if="state === 'canceled'">*</template>
    </template>

    <template v-else-if="state === 'active'">
      {{ price === 0 ? $t('Subscribed for free') : $t('Subscribed for {price}', { price: priceWithCurrency }) }}
      <template v-if="subscription.donation > 0">*</template>
    </template>

    <template v-else-if="state === 'suspended'">
      {{ $t('Suspended') }}
    </template>
  </button>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'NewspaperSubscriptionButton',

  props: {
    newspaper: Object
  },

  computed: {
    subscription() {
      return this.$store.getters.getNewspaperSubscription(this.newspaper)
    },

    state() {
      return this.subscription ? this.subscription.state : null
    },

    buttonTitle() {
      if (this.state === 'active') {
        return 'Change subscription'
      }
      if (this.state === 'canceled') {
        return 'Renew subscription'
      }
      if (this.state === 'suspended') {
        return 'Not enough credits, resolve it'
      }
      return false
    },

    price() {
      let price =  ~~this.newspaper.price.split('.')[0]
      if (this.subscription && this.subscription.donation) {
        price += ~~this.subscription.donation.split('.')[0]
      }
      return price
    },

    priceWithCurrency() {
      return `${this.price} Kč`
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.newspaper-subscription-button

  //- when newspaper is subscribed
  &.is-subscribed
    +button(primary, small)

  //- when newspeper is suspended
  &.is-suspended
    +button(primary, small)

    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  &.to-subscribe,
  &.is-canceled
    +button(secondary, small)

</style>
