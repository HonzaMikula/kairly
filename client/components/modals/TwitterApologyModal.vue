<template>
  <DialogWindow
    v-if="active"
    custom-class="twitter-apology"
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Twitter import is not ready yet') }}</h1>
    </template>

    <p>
      {{ $t('We are sorry, but we are still working on the integration with Twitter.') }}
    </p>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'TwitterApologyModal',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin]
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.modal-dialog.twitter-apology
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
