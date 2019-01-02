<template>
  <div class="newspaper-subscription">
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
      <template v-if="subscription === false">
        {{ $t('Subscribe for') }} {{ newspaper.price.split('.')[0] }} Kč
      </template>

      <template v-else-if="subscription.state === 'active'">
        {{ $t('Subscribed for') }} {{ newspaper.price.split('.')[0] }} Kč
      </template>

      <template v-else-if="subscription.state === 'canceled'">
        {{ $t('Subscribe for') }} {{ newspaper.price.split('.')[0] }} Kč*
      </template>

      <template v-else-if="subscription.state === 'suspended'">
        {{ $t('Suspended') }}
      </template>
    </button>

    <!-- <button
      v-if="subscription"
      :class="{
        'is-subscribed': subscription.state === 'active',
        'is-canceled': subscription.state === 'canceled',
        'is-suspended': subscription.state === 'suspended',
      }"
      @click="subscription.state == 'canceled' ? subscribe() : unsubscribe()">
      <span class="default">
        <span v-if="subscription.state == 'active'">{{ $t('Subscribed for') }} {{ newspaper.price.split('.')[0] }} Kč</span>
        <span v-if="subscription.state == 'suspended'">{{ $t('Suspended') }}</span>
        <span v-if="subscription.state == 'canceled'">{{ $t('Canceled') }}</span>
      </span>
      <span
        v-if="subscription.state == 'active' || subscription.state == 'suspended'"
        class="on-hover">
        {{ $t('Unsubscribe') }}
      </span>
      <span
        v-if="subscription.state == 'canceled'"
        class="on-hover"
        v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
        :title="$t('Subscription last till {to}', {to: subscription.to})">
        {{ $t('Renew') }}
      </span>
    </button>

    <button
      v-else
      class="to-subscribe"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :title="newspaper.price"
      @click="openModal">
      {{ $t('Subscribe for') }}
      {{ newspaper.price.split('.')[0] }} Kč
    </button> -->

    <portal to="modal" v-if="isSubscriptionConfirmationModalOpen">
      <SubscriptionConfirmation
        :newspaper="newspaper"
        :subscription="subscription"
        :closeModal="closeModal"
      >
      </SubscriptionConfirmation>
    </portal>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import SubscriptionConfirmation from '@/components/modals/SubscriptionConfirmation'

export default {
  name: 'NewspaperSubscription',

  props: {
    newspaper: Object
  },

  components: {
    SubscriptionConfirmation
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
    }
  },

  data() {
    return {
      isSubscriptionConfirmationModalOpen: null
    }
  },

  methods: {
    unsubscribe() {
      this.$store.dispatch('unsubscribeNewspaper', {
        fullName: this.newspaper.fullName
      })
      document.activeElement.blur()
    },

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
.newspaper-subscription

  //- when newspaper is subscribed
  button.is-subscribed
    +subscribed-button

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when newspeper is suspended
  button.is-suspended
    +subscribed-button

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  button.to-subscribe,
  button.is-canceled
    +subscribe-button

</style>
