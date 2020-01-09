<template>
  <DialogWindow
    v-if="active"
    custom-class="share-modal"
    ignoreBackgroundClick
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Share') }}</h1>
    </template>

    <div>
      <h1>{{ title }}</h1>
      <ul>
        <li v-for="post in posts" :key="post.post.id">
          • <a :href="post.post.source">{{ post.post.content.title }}</a>
          <button @click="removeItem(post.post.id)" class="remove"></button>
        </li>
      </ul>

      <p>{{ url }}</p>
    </div>

    <template #footer>
      <a href="" class="copy" @click.prevent="copyToClipboard()">Copy</a>
      <a :href="`https://www.facebook.com/sharer/sharer.php?u=${url}`" target="_blank" class="facebook">Facebook</a>
      <a :href="`https://twitter.com/intent/tweet?text=${content}&url=${url}`" target="_blank" class="twitter">Twitter</a>
      <a :href="`https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}&summary=${content}`" class="linkedin" target="_blank">LinkedIn</a>
      <a :href="`mailto:?subject=${title}&body=${content}%0D%0A%0D%0A${url}`" class="send-by-email">Send by email</a>
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

  data() {
    return {
      posts: this.issue.posts,
    }
  },

  computed: {
    title() {
      return `${this.issue.newspaper.title} #${this.issue.number}`
    },

    url() {
      return `https://kairly.com/${this.issue.newspaper.fullName}/${this.issue.number}`
    },

    content() {
      let content = ''
      this.issue.posts.forEach(function (post) {
        content += '• '+ post.post.content.title +'\n'
      })
      return encodeURIComponent(content)
    }
  },

  mixins: [ModalMixin],

  methods: {
    removeItem(id) {
      this.posts.splice(this.posts.findIndex(function(i){
          return i.post.id === id
      }), 1)
    },

    async copyToClipboard() {
      try {
        await this.$copyText(this.content)
      } catch (e) {
        console.error(e)
      }
    }
  }
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
      position: relative
      
      margin-bottom: $baseline / 4
      padding-right: $baseline

      font-size: $fs-0

      a
        display: inline-block
        margin-left: $baseline / 4

        color: darken($c-base, 20%)

      
      &:hover button
        display: inline-block

      //- remove button
      button
        position: absolute

        display: none
        background: transparent
        border: 0
        color: #aaa

        cursor: pointer
        line-height: $baseline

        &:hover,
        &:focus
          color: #333

        &::before
          +fa-icon()
          @extend .fas
          content: fa-content($fa-var-times)


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
