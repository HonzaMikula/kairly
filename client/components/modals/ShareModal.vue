<template>
  <DialogWindow
    v-if="active"
    custom-class="share-modal"
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Share') }}</h1>
    </template>

    <h1>{{ issue.newspaper.title }} #{{ issue.number }}</h1>
    <ul>
      <li v-for="post in issue.posts" :key="post.id">
        {{ post.post.content.title }}
      </li>
    </ul>

    <template #footer>
      <a href="" class="copy">Copy</a>
      <a href="" class="facebook">Facebook</a>
      <a href="" class="twitter">Twitter</a>
      <a href="" class="linkedin">LinkedIn</a>
      <a href="" class="send-by-email">Send by email</a>
    </template>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'ShareModal',

  components: {
    DialogWindow
  },

  props: {
    issue: Object
  },

  mixins: [ModalMixin]
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.modal-dialog.share-modal
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

    //- heading
    h1
      margin-bottom: $baseline / 2

      font-weight: 600
      font-size: $fs-1

    li
      margin-bottom: $baseline / 4

      font-size: $fs--1

      &::before
        content: ' • '

  //- Footer
  footer
    padding: 0
    display: flex
    justify-content: space-between

    a
      padding: $baseline/2 $baseline

      color: darken($c-base, 30%)

      font-size: $fs--1

      &:hover,
      &:focus
        background: #ddd

      &::before
        margin-bottom: $baseline / 4

        font-size: $fs-1

      &.copy::before
        +fa-icon()
        @extend .fas
        content: fa-content($fa-var-copy)
        display: block
      
      &.facebook::before
        +fa-icon()
        @extend .fab
        content: fa-content($fa-var-facebook)
        display: block

      &.twitter::before
        +fa-icon()
        @extend .fab
        content: fa-content($fa-var-twitter)
        display: block

      &.linkedin::before
        +fa-icon()
        @extend .fab
        content: fa-content($fa-var-linkedin)
        display: block

      &.send-by-email::before
        +fa-icon()
        @extend .fas
        content: fa-content($fa-var-at)
        display: block


</style>
