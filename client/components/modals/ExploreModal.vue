<template>
  <DialogWindow
    v-if="active"
    custom-class="explore-modal"
    @close="closeModal"
  >
    <template #header>
      <h1>{{ category.name }}</h1>
    </template>

    <AuthorWidget
      v-for="author in category.authors.slice(limit)"
      :key="author.id"
      :author="author"
    />
  </DialogWindow>
</template>

<script>
import AuthorWidget from '@/components/widgets/AuthorWidget'
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'ExploreModal',

  components: {
    DialogWindow,
    AuthorWidget
  },

  mixins: [ModalMixin],

  props: {
    category: Object,
    limit: Number
  },

  head () {
    return {
      title: this.category ? this.category.name : this.$t('Explore')
    }
  }
}
</script>

<style lang="sass">
.explore-modal .modal-dialog
  max-width: auto

.explore-modal main
  position: relative

  padding: $baseline $baseline * 3/4
  overflow: auto
  -webkit-overflow-scrolling: touch

  @media (max-width: $mobile)
    padding: $baseline / 2 0

</style>
