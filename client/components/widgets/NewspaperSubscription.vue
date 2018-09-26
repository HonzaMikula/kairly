<template>
  <div class="newspaper-subscription">
    <button
      v-if="subscription"
      :class="{'is-subscribed': subscription.renewal, 'is-canceled': !subscription.renewal}"
      @click="toggle()">
      <span class="default">
        <span v-if="subscription.renewal">Subscribed</span>
        <span v-else>Canceled</span>
      </span>
      <span class="on-hover" v-if="subscription.renewal">Unsubscribe</span>
      <span
        v-else
        class="on-hover"
        v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
        :title="`Subscribtion last till ${subscription.to}`">
        Renew
      </span>
    </button>

    <button
      v-else
      class="to-subscribe"
      @click="toggle()">
      Subscribe
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

  data() {
    return {
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    subscription() {
      return this.$store.getters.getNewspaperSubscription(this.newspaper)
    }
  },

  methods: {
    toggle() {
      if (this.subscription && this.subscription.renewal) {
          this.$store.dispatch('unsubscribeNewspaper', this.newspaper.fullName)
      } else {
          this.$store.dispatch('subscribeNewspaper', this.newspaper.fullName)
      }
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

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

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

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

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

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1
</style>
