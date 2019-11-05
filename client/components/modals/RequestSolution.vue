<template>
  <DialogWindow
    v-if="active"
    custom-class="request-solution"
    ignoreBackgroundClick
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Request solution') }}</h1>
    </template>

    <iframe 
      src="https://docs.google.com/forms/d/e/1FAIpQLSdedtdKD22tCx0ZVTLQuIgN0lzqiyrTXC77gcM_GmWyCN5hiw/viewform?embedded=true"
      width="100%"
      height="1000px"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
    >
      Loading…
    </iframe>
  </DialogWindow>
</template>


<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'RequestSolutionModal',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin],

  data() {
    return {
      isSignInModalOpen: false,
    }
  },

  methods: {
    
  }
}
</script>

<style lang="sass">
//- Imports -//
@import './styles/components/buttons'

//- Styles -//
.modal-dialog.request-solution
  background: #f5f5f5
  max-width: 90vw

  min-width: 640px

  @media (max-width: $mobile)
    width: 90vw

  main
    padding: $baseline/4

  div
    margin-bottom: $baseline / 2

    &:last-of-type
      margin-bottom: 0

</style>
