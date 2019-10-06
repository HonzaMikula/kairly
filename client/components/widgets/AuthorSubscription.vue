<template>
  <div class="author-subscription-view">
    <button
      :class="{
        'to-subscribe': !subscription,
        'is-subscribed': state === 'active',
        'is-canceled': state === 'canceled',
        'is-suspended': state === 'suspended',
      }"
      v-b-tooltip
      :title="buttonTitle"
      @click="openModal"
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

    <AuthorSubscriptionModal
      :active.sync="isSubscriptionConfirmationModalOpen"
      :author="author"
      :subscription="subscription"
    />
  </div>
</template>

<script>
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AuthorSubscriptionModal from '@/components/modals/AuthorSubscriptionModal'

export default {
  name: 'AuthorSubscription',

  props: {
    author: Object
  },

  components: {
    AuthorSubscriptionModal
  },

  mixins: [PeriodicityMixin],

  computed: {
    subscription() {
      return this.$store.getters.getAuthorSubscription(this.author)
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
      // todo use decimal types
      let price =  ~~this.author.price.split('.')[0]
      if (this.subscription && this.subscription.donation) {
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
      this.isSubscriptionConfirmationModalOpen = false
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.author-subscription-view
  button
    white-space: nowrap

  //- when newspaper is subscribed
  button.is-subscribed
    +button(primary, small)

  //- when newspeper is suspended
  button.is-suspended
    +button(primary, small)

    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)
    color: #fff

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  button.to-subscribe,
  button.is-canceled
    +button(secondary, small)

</style>
