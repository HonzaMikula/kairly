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
        {{ $t('Subscribe for') }} {{ newspaperPrice }}
      </template>

      <template v-else-if="subscription.state === 'active'">
        {{ $t('Subscribed for') }} {{ newspaperPrice }}
      </template>

      <template v-else-if="subscription.state === 'canceled'">
        {{ $t('Subscribe for') }} {{ newspaperPrice }}*
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

    newspaperPrice() {
      if (this.newspaper.price.split('.')[0] == 0)
        return 'free'
      else
        return this.newspaper.price.split('.')[0] + ' Kč'
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
.newspaper-subscription

  //- when newspaper is subscribed
  button.is-subscribed
    +subscribed-button

  //- when newspeper is suspended
  button.is-suspended
    +subscribed-button

    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

  //- when newspaper is ready to be subsribed
  //- when newspeper is canceled
  button.to-subscribe,
  button.is-canceled
    +subscribe-button

</style>
