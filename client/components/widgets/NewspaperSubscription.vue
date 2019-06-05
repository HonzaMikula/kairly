<template>
  <div class="newspaper-subscription">
    <button
      :class="{
        'to-subscribe': subscription === false,
        'is-subscribed': subscription.state === 'active',
        'is-canceled': subscription.state === 'canceled',
        'is-suspended': subscription.state === 'suspended',
      }"
      v-b-tooltip
      :title="buttonTitle"
      @click="openModal"
    >
      <template v-if="subscription === false || subscription.state === 'canceled'">
        {{ price === 0 ? $t('Subscribe for free') : $t('Subscribe for {price}', { price: priceWithCurrency }) }}<template v-if="subscription.state === 'canceled'">*</template>
      </template>

      <template v-else-if="subscription.state === 'active'">
        {{ price === 0 ? $t('Subscribed for free') : $t('Subscribed for {price}', { price: priceWithCurrency }) }}<template v-if="subscription.donation > 0">*</template>
      </template>


      <template v-else-if="subscription.state === 'suspended'">
        {{ $t('Suspended') }}
      </template>
    </button>

    <portal to="modal" v-if="isSubscriptionConfirmationModalOpen">
      <NewspaperSubscriptionDialog
        :newspaper="newspaper"
        :subscription="subscription"
        :closeModal="closeModal"
      >
      </NewspaperSubscriptionDialog>
    </portal>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import NewspaperSubscriptionDialog from '@/components/modals/NewspaperSubscription'

export default {
  name: 'NewspaperSubscription',

  props: {
    newspaper: Object
  },

  components: {
    NewspaperSubscriptionDialog
  },

  computed: {
    subscription() {
      const subscription = this.$store.getters.getNewspaperSubscription(this.newspaper)
      return subscription ? subscription : false
    },

    buttonTitle() {
      if (this.subscription.state === 'active') {
        return 'Change subscription'
      }
      else if (this.subscription.state === 'canceled') {
        return 'Renew subscription'
      }
      else if (this.subscription.state === 'suspended') {
        return 'Not enough credits, resolve it'
      }
      else {
        return false
      }
    },

    price() {
      let price =  ~~this.newspaper.price.split('.')[0]
      if (this.subscription.donation) {
        price += ~~this.subscription.donation.split('.')[0]
      }
      return price
    },

    priceWithCurrency() {
      return `${this.price} Kč`
    }
  },

  data() {
    return {
      isSubscriptionConfirmationModalOpen: null
    }
  },

  methods: {
    openModal() {
      this.isSubscriptionConfirmationModalOpen = true
      document.activeElement.blur()
    },

    closeModal() {
      this.isSubscriptionConfirmationModalOpen = null
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.newspaper-subscription

  //- when newspaper is subscribed
  button.is-subscribed
    +button(primary, small)

  //- when newspeper is suspended
  button.is-suspended
    +button(primary, small)

    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  button.to-subscribe,
  button.is-canceled
    +button(secondary, small)

</style>
