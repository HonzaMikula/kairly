<template>
  <div class="author-subscription-view">
    <button
      :class="{
        'to-subscribe': subscription === false,
        'is-subscribed': subscription.state === 'active',
        'is-canceled': subscription.state === 'canceled',
        'is-suspended': subscription.state === 'suspended',
      }"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :title="buttonTitle"
      @click="openModal"
    >
      <template v-if="subscription === false || subscription.state === 'canceled'">
        {{ price === 0 ? $t('Subscribe for free') : $t('Subscribe for {price}', { price: priceWithCurrency }) }}<template v-if="subscription.state === 'canceled'">*</template>
      </template>

      <template v-else-if="subscription.state === 'active'">
        {{ price === 0 ? $t('Subscribed for free') : $t('Subscribed for {price}', { price: priceWithCurrency }) }}
      </template>

      <template v-else-if="subscription.state === 'suspended'">
        {{ $t('Suspended') }}
      </template>
    </button>

    <portal to="modal" v-if="isSubscriptionConfirmationModalOpen">
      <AuthorSubscriptionDialog
        :author="author"
        :subscription="subscription"
        :closeModal="closeModal"
      >
      </AuthorSubscriptionDialog>
    </portal>
  </div>
</template>

<script>
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AuthorSubscriptionDialog from '@/components/modals/AuthorSubscription'

export default {
  name: 'AuthorSubscription',

  props: {
    author: Object
  },

  components: {
    AuthorSubscriptionDialog
  },

  mixins: [PeriodicityMixin],

  computed: {
    frequency() { return this.subscription && this.subscription.periodicity.frequency },
    dow() { return this.subscription && this.subscription.periodicity.dow },
    time() { return this.subscription && this.subscription.periodicity.time },

    subscription() {
      const subscription = this.$store.getters.getAuthorSubscription(this.author)
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
      return ~~this.author.price.split('.')[0]
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

.author-subscription-view
  //- when newspaper is subscribed
  button.is-subscribed
    +button(primary, small)

  //- when newspeper is suspended
  button.is-suspended
    +button(secondary, small)

    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  button.to-subscribe,
  button.is-canceled
    +button(secondary, small)

</style>
