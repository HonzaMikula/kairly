<template>
  <div class="newspaper-subscription">
    <button
      v-if="subscription"
      :class="{
        'is-subscribed': subscription.state === 'active',
        'is-canceled': subscription.state === 'canceled',
        'is-suspended': subscription.state === 'suspended',
      }"
      @click="subscription.state == 'canceled' ? subscribe() : unsubscribe()">
      <span class="default">
        <span v-if="subscription.state == 'active'">{{ $t('Subscribed') }}</span>
        <span v-if="subscription.state == 'suspended'">{{ $t('Suspended') }}</span>
        <span v-if="subscription.state == 'canceled'">{{ $t('Canceled') }}</span>
      </span>
      <span
        v-if="subscription.state == 'active' || subscription.state == 'suspended'"
        class="on-hover"
      >{{ $t('Unsubscribe') }}</span>
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
      @click="subscribe()">
      {{ $t('Subscribe') }}
    </button>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'NewspaperSubscription',

  props: {
    newspaper: Object
  },

  computed: {
    subscription() {
      return this.$store.getters.getNewspaperSubscription(this.newspaper)
    }
  },

  methods: {
    subscribe() {
      this.$store.dispatch('subscribeNewspaper', this.newspaper.fullName)
      document.activeElement.blur()
    },

    unsubscribe() {
      this.$store.dispatch('unsubscribeNewspaper', this.newspaper.fullName)
      document.activeElement.blur()
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

  //- when newspeper is canceled
  button.is-canceled
    +subscribed-button

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when newspaper is ready to be subsribed
  button.to-subscribe
    +subscribe-button

</style>
