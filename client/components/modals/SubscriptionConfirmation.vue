<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="subscription-confirmation">
      <header>
        <h1 v-if="!subscription.state">Subscribe newspaper</h1>
        <h1 v-else-if="subscription.state === 'active'">Change or cancel subscription</h1>
        <h1 v-else-if="subscription.state === 'canceled'">Renew subscription</h1>
        <h1 v-else-if="subscription.state === 'suspended'">Resolve suspended subscription</h1>

        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <main>
        <section>
          <h2>You want to subscribe to</h2>
          <p>{{ newspaper.title }}</p>

          <h2>It will cost you</h2>
          <p>{{ newspaper.price.split('.')[0] }} Kč per month</p>
          <p>* You can cancel subscription any time</p>
        </section>

        <section class="donate-more">
          <h2>To support exceptional journalist, donate more</h2>
          <div>
            <input v-model="donation" type="number" placeholder="Your donation" /> Kč
            <br />
            per month
          </div>
        </section>
      </main>
      <footer class="subscription-confirmation--footer">
        <template v-if="!subscription.state">
          <button>Subscribe newspaper</button>
        </template>

        <template v-else-if="subscription.state === 'active'">
          <button>Change subscription</button>

          <button class="cancel">Cancel subscription</button>
        </template>

        <template v-else-if="subscription.state === 'canceled'">
          <button>
            Renew subscription
          </button>
        </template>

        <template v-else-if="subscription.state === 'suspended'">
          <button>
            Cancel subscription
          </button>
        </template>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'SubscriptionConfirmationDialog',

  props: {
    newspaper: Object,
    subscription: Object,
    closeModal: Function
  },

  components: {
    DialogWindow
  },

  data() {
    return {
      donation: null
    }
  },

  methods: {
    subscribe() {
      this.$store.dispatch('subscribeNewspaper', {
        fullName: this.newspaper.fullName,
        donation: this.donation ? this.donation : null
      })
      this.closeModal()
    },
  }
}
</script>

<style lang="sass">
modal-dialog.subscription-confirmation
  display: block

  main
    text-align: center

    //- Close button
    button-icon.close
      position: absolute
      right: 0
      top: 0

      height: $baseline
      width: $baseline

      color: #999

      &:hover,
      &:focus
        color: #000

    h2
      margin-bottom: $baseline / 4

    //- bold text
    h2 + p
      margin-bottom: $baseline

      font-size: $fs-3
      font-weight: 600

    h2 + p + p
      font-size: $fs--1
      margin-top: -($baseline)
      margin-bottom: $baseline

    > section
      padding: $baseline $baseline 0 $baseline


    //- Donate More
    .donate-more
      padding: $baseline/2 $baseline

      background: #f5f5f5

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
  > footer
    background: #fff

    //- confirm button
    button.confirm
      +subscribed-button

      height: $baseline * 1.25

      font-size: $fs-0
      line-height: $baseline * 1.25

    button.cancel
      background: $c-red

    //- foot note
    button + p
      font-size: $fs--1
</style>
