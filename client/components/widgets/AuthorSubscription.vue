<template>
  <div>
    <AuthorSubscriptionButton
      :author="author"
      @click="openModal"
    />

    <AuthorSubscriptionModal
      :active.sync="isModalOpen"
      :author="author"
    />
  </div>
</template>

<script>
import AuthorSubscriptionButton from '@/components/widgets/AuthorSubscriptionButton'
import AuthorSubscriptionModal from '@/components/modals/AuthorSubscriptionModal'

export default {
  name: 'AuthorSubscription',

  props: {
    author: Object
  },

  components: {
    AuthorSubscriptionButton,
    AuthorSubscriptionModal
  },

  data() {
    return {
      isModalOpen: false
    }
  },

  methods: {
    openModal() {
      this.isModalOpen = true
      document.activeElement.blur()
    }
  }
}
</script>
