<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="join-us">
      <header>
        <h1>Are you interested in Kairly?</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <div>
        <p>Here are ways how you can help us:</p>
        <ul>
          <li>
            Join our
            <a href="https://www.facebook.com/groups/276916213077456/">Facebook group</a>
          </li>
          <li>
            Participate in
            <a href="mailto:jan.mikula@hotmail.com?subject=Kairly user testing&body=Hi, I would like to do user testing for Kairly.">user testing over Skype</a>
          </li>
          <li>
            Request to join
            <a href="mailto:jan.mikula@hotmail.com?subject=Kairly join beta&body=Hi, I would like to join Kairly private beta.">private beta program</a>
          </li>
        </ul>
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

  > div
    padding: $baseline

  p
    margin-bottom: $baseline

  li
    list-style: disc
    margin-left: $baseline

    font-size: $fs--1
    white-space: nowrap

    a
      color: $c-base

      text-decoration: underline

      &:focus,
      &:hover
        text-decoration: none

</style>
