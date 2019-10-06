<template>
  <div>
    <NewspaperSubscriptionButton
      :newspaper="newspaper"
      @click="openModal"
    />

    <NewspaperSubscriptionModal
      :active.sync="isModalOpen"
      :newspaper="newspaper"
    />
  </div>
</template>

<script>
import NewspaperSubscriptionButton from '@/components/widgets/NewspaperSubscriptionButton'
import NewspaperSubscriptionModal from '@/components/modals/NewspaperSubscriptionModal'

export default {
  name: 'NewspaperSubscription',

  props: {
    newspaper: Object
  },

  components: {
    NewspaperSubscriptionButton,
    NewspaperSubscriptionModal
  },

  data() {
    return {
      isModalOpen: null
    }
  },

  methods: {
    openModal() {
      this.isModalOpen = true
      document.activeElement.blur()
    },
  }
}
</script>
