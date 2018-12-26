<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="subscription-confirmation">
      <main>
        <button-icon class="close" @click="closeModal()"></button-icon>
        <section>
          <h2>You want to subscribe to</h2>
          <p>Malostranské noviny</p>

          <h2>It will cost you</h2>
          <p>25 credits per month</p>
        </section>

        <section class="donate-more">
          <h2>To support exceptional journalist, donate more</h2>
          <div>
            <input type="number" placeholder="Number of credits" />
            <br />
            credits per month
          </div>
        </section>
      </main>
      <footer class="subscription-confirmation--footer">
        <button class="confirm" @click="closeModal()">Confirm subscription</button>
        <p>* You can cancel subscription any time</p>
      </footer>
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

    //- foot note
    button + p
      font-size: $fs--1
</style>
