<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="join-us">
      <header>
        <h1>Are you interested in Kairly?</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <div>
        <h3>Participate in user testing</h3>
        <p>
          We are doing 30 - 60 minutes user testing interviews over Skype (or some other communication tool).
          We will give you access to Kairly. You will share screen with us. We will observe how you use Kairly.
          Together we will discuss what you like, what you don't like and how we can improve the app.
        </p>

        <p>
          <a href="mailto:info@kairly.com?subject=Kairly user testing&body=Hi, I would like to do user testing for Kairly.">Schedule user testing interview</a>
        </p>

        <h3>Join private beta</h3>
        <p>
          We are inviting limited number of people to use Kairly and give us feedback about the app.
          Based on the feedback we are improving the app every week. Although there can be many bugs in the app,
          you can experience our ideas how to improve current state of journalism.
        </p>
        <p>
          <a href="mailto:info@kairly.com?subject=Kairly join beta&body=Hi, I would like to join Kairly private beta.">Join private beta</a>
        </p>

        <h3>Join Facebook group</h3>
        <p>
          We have Kairly group on Facebook, where we regularly share what's new in Kairly and what we are planning for next weeks.
          It's place where people give us feedback and propose ideas, how we can improve Kairly.
        </p>

        <p>
          <a href="https://www.facebook.com/groups/276916213077456/">Join Facebook group</a>
        </p>

      </div>
    </modal-dialog>
  </dialog-window>
</template>


<script>
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'JoinUsDialog',

  props: {
    closeModal: Function
  },

  components: {
    DialogWindow
  }
}
</script>

<style lang="sass">
modal-dialog.join-us
  max-width: 600px

  > div
    padding: $baseline
    background: #fff

  h3
    margin-top: $baseline
    font-weight: 600
    font-size: $fs-1

    &:first-of-type
      margin-top: 0

  p
    margin-bottom: $baseline / 2

    line-height: 1.42


  a
    display: inline-block
    border-radius: 5px
    padding: 0 $baseline/2

    background: $c-base
    border: 1px solid $c-base
    color: #fff

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0
    line-height: $baseline

    &:focus,
    &:hover
      background: darken($c-base, 10%)

</style>
