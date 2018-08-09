<template>
  <dialog-window :onClose="closeModal">
    <explore-modal-view role="dialog" @click.stop>
      <h2>{{ category.name }}</h2>

      <button-close tabindex="0" role="button" @click="onClose">X</button-close>

      <AuthorWidget
        v-for="author in category.authors"
        :key="author.id"
        :author="author"
      />


    </explore-modal-view>
  </dialog-window>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'

import DialogWindow from '@/components/modals/Dialog'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'ExploreModal',

  props: {
    onClose: Function,
    category: Object,
  },

  metaInfo() {
      return {
        title: this.category ? this.category.name : 'Explore'
      }
  },

  components: {
    DialogWindow,
    AuthorWidget
  },

  computed: mapGetters(['user']),
}
</script>

<style lang="sass">
explore-modal-view
  position: relative

  padding: $baseline
  background: #fff
  max-height: 80vh
  overflow-y: auto

  button-close
    font-size: $fs-2
    font-weight: 600
    cursor: pointer
    position: absolute
    top: 0
    right: 0
    width: 60px
    height: 60px
    border: 1px solid gray
    box-sizing: border-box
    text-align: center
    display: block
    padding-top: 15px
    z-index: 999

    &:hover
      background: #eee


</style>
