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
      <template v-if="subscription === false">
        {{ $t('Subscribe for') }} {{ authorPrice }}
      </template>

      <template v-else-if="subscription.state === 'active'">
        {{ $t('Subscribed for') }} {{ authorPrice }}
      </template>

      <template v-else-if="subscription.state === 'canceled'">
        {{ $t('Subscribe for') }} {{ authorPrice }}*
      </template>

      <template v-else-if="subscription.state === 'suspended'">
        {{ $t('Suspended') }}
      </template>
    </button>

    <portal to="modal" v-if="isSubscriptionConfirmationModalOpen">
      <AuthorSubscriptionConfirmation
        :author="author"
        :subscription="subscription"
        :closeModal="closeModal"
      >
      </AuthorSubscriptionConfirmation>
    </portal>
  </div>
</template>

<script>
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AuthorSubscriptionConfirmation from '@/components/modals/AuthorSubscriptionConfirmation'

export default {
  name: 'AuthorSubscription',

  props: {
    author: Object
  },

  components: {
    AuthorSubscriptionConfirmation
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

    authorPrice() {
      if (this.author.price.split('.')[0] == 0)
        return 'free'
      else
        return this.author.price.split('.')[0] + ' Kč'
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
.author-subscription-view
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
