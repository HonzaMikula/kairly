<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="subscription-confirmation">
      <main>
        <h2>You want to subscribe to</h2>
        <p>Malostranské noviny</p>

        <h2>It will cost you</h2>
        <p>25 credits per month</p>

        <h2>To support exceptional journalist, donate more</h2>
        <div>
          <input type="number" placeholder="Number of credits" />
          <br />
          credits per month
        </div>

        <button class="confirm" @click="closeModal()">Confirm subscription</button>
        <br />
        <button class="cancel" @click="closeModal()">Cancel</button>
        <p>* You can cancel subscription any time</p>
      </main>
    </modal-dialog>
  </dialog-window>
</template>


<script>
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'SubscriptionConfirmationDialog',

  props: {
    closeModal: Function
  },

  components: {
    DialogWindow
  },

  data() {
    return {
      invalidCredentials: false,
      username: null,
      password: null
    }
  },

  methods: {

  }
}
</script>

<style lang="sass">
modal-dialog.subscription-confirmation
  display: block

  main
    padding: $baseline

    text-align: center

    h2
      margin-bottom: $baseline / 4

    //- bold text
    h2 + p
      margin-bottom: $baseline

      font-size: $fs-3
      font-weight: 600

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
      margin-bottom: $baseline

      font-size: $fs--1

    //- confirm button
    button.confirm
      +subscribed-button

      height: $baseline * 1.5

      font-size: $fs-1
      line-height: $baseline * 1.5

    button.cancel
      background: transparent
      border: 0

      font-family: $ff-sans
      font-size: $fs-0
      cursor: pointer

    //- foot note
    button + p
      margin-top: $baseline / 2

      font-size: $fs--1

</style>
