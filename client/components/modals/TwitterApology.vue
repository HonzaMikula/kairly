<template>
  <DialogWindow @close="closeModal">
    <modal-dialog
      role="dialog"
      class="twitter-apology"
      @click.stop
    >
      <header>
        <h1>{{ $t('Twitter import is not ready yet') }}</h1>
        <button-close
          tabindex="0"
          role="button"
          @click="closeModal"
        />
      </header>
      <main>
        <p>
          {{ $t('We are sorry, but we are still working on the integration with Twitter.') }}
        </p>
      </main>
    </modal-dialog>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'

export default {
  name: 'TwitterApologyDialog',

  props: {
    closeModal: Function
  },

  components: {
    DialogWindow
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

modal-dialog.twitter-apology
  max-width: 600px

  > header h1
    @media (max-width: $mobile)
      padding: 0 $baseline/2

  main
    padding: $baseline / 2
    overflow: auto
    -webkit-overflow-scrolling: touch

    background: #fff

    @media (max-width: $mobile)
      padding: $baseline/2

    p

      a
        color: $c-base

        text-decoration: underline

        &:hover,
        &:focus
          text-decoration: none


</style>
