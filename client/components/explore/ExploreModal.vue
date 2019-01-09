<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" class="explore" @click.stop>
      <header>
        <h1>{{ category.name }}</h1>

        <button-close tabindex="0" role="button" @click="closeModal"></button-close>
      </header>

      <explore-modal-view>

        <AuthorWidget
          v-for="author in category.authors.slice(limit)"
          :key="author.id"
          :author="author"
        />
      </explore-modal-view>
    </modal-dialog>
  </dialog-window>
</template>

<script>


import DialogWindow from '@/components/modals/Dialog'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'ExploreModal',

  props: {
    closeModal: Function,
    category: Object,
    limit: Number
  },

  head() {
    return {
      title: this.category ? this.category.name : this.$t('Explore')
    }
  },

  components: {
    DialogWindow,
    AuthorWidget
  }
}
</script>

<style lang="sass">
modal-dialog.explore
  max-width: auto

explore-modal-view
  position: relative

  padding: $baseline $baseline * 3/4
  overflow: auto
  -webkit-overflow-scrolling: touch

  @media (max-width: $mobile)
    padding: $baseline / 2 0


</style>
