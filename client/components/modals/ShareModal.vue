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
        <li v-for="post in listOfPosts()" :key="post.post.id">
          <template v-if="post.post.content.title">
            <nuxt-link :to="{ name: 'author-post', params: { author: post.post.author.id, post: post.post.slug }}">
              {{ post.post.content.title }}
            </nuxt-link>
          </template>

          <template v-else>
            {{ post.post.author.name }}: <span v-html="post.post.content.content"></span>
          </template>
          
          <button @click="removeItem(post.post.id)" class="remove"></button>
        </li>
      </ul>

      <p class="share--url">{{ url }}</p>
    </div>

    <div class="share--show-more">
      <button
        v-if="(tailPostsCount() > 0 && !isExpanded)"
        @click.prevent="isExpanded = true">
        {{ $t('Show more') }} ({{tailPostsCount()}})
      </button>
    </div>

    <template #footer>
      <a href="" class="copy" @click.prevent="copyToClipboard()">{{ $t('Copy') }}</a>
      <a :href="`https://www.facebook.com/sharer/sharer.php?u=${url}`" target="_blank" class="facebook">Facebook</a>
      <a :href="`https://twitter.com/intent/tweet?text=${encodedContent()}&url=${url}`" target="_blank" class="twitter">Twitter</a>
      <a :href="`https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}&summary=${encodedContent()}`" class="linkedin" target="_blank">LinkedIn</a>
      <a :href="`mailto:?subject=${title}&body=${encodedContent()}%0D%0A%0D%0A${url}`" class="send-by-email">Email</a>
    </template>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

const POST_LIMIT = 5

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
      isExpanded: false
    }
  },

  computed: {
    title() {
      return `${this.issue.newspaper.title} #${this.issue.number}`
    },

    url() {
      return `https://kairly.com/${this.issue.newspaper.fullName}/${this.issue.number}`
    }
  },

  mixins: [ModalMixin],

  methods: {
    content() {
      let content = ''
      this.posts.forEach(function (post) {
        if (post.post.content.title) {
          content += `• ${post.post.content.title} \n`
        }
        else {
          var div = document.createElement("div") // striping HTML
          div.innerHTML = post.post.content.content
          var text = div.textContent || div.innerText || ""
          content += `• ${post.post.author.name}: ${text} \n`
        }
      })

      return content
    },

    encodedContent(){
      return encodeURIComponent(this.content())
    },

    tailPostsCount() {
      return Math.max(0, this.posts.length - POST_LIMIT)
    },

    listOfPosts() {
      if (!this.isExpanded)
        return this.posts.slice(0, POST_LIMIT)
      else
        return this.posts
    },

    removeItem(id) {
      this.posts.splice(this.posts.findIndex(function(i){
          return i.post.id === id
      }), 1)
    },

    async copyToClipboard() {
      try {
        const textToShare = this.title + '\n'+ this.content() + this.url
        await this.$copyText(textToShare)
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
    position: relative

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
      padding: 0 $baseline 0 $baseline/2

      font-size: $fs-0

      &::before
        position: absolute
        left: 0

        line-height: $baseline
        content: ' • '

      a
        display: inline

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
  
  .share--url
    overflow: auto

    font-size: $fs--1

  .share--show-more
    margin-top: $baseline / 2

    button
      +button(secondary, small)

      background: #eee
      border: 0

      &:hover,
      &:focus
        background: #ddd
        color: #000 


  //- Footer
  footer
    padding: 0
    display: flex
    justify-content: center
    a
      padding: $baseline/2 $baseline

      color: darken($c-base, 30%)

      font-size: $fs--1

      @media (max-width: $mobile)
        padding: $baseline/2

        font-size: $fs--2
        line-height: 1.42

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
