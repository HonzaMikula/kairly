<template>
  <PostBase :post="post">

        <div class="editorial-post-editor--content">
          <input
            v-model="title"
            type="text"
            :placeholder="$t('Title')"
          />
          <rich-editor
            v-model="content"
            :options="options"
          />
        </div>

    <template #page-controls><slot name="page-controls"></slot></template>
    <template #global-controls><slot name="global-controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from '@/components/posts/PostBase'

export default {
  name: 'CommentEditor',

  props: {
    post: Object,
  },

  components: {
    PostBase
  },

  data() {
    return {
      title: this.post.content.title,
      content: this.post.content.content,
      options: {
        placeholder: this.$t('Editorial'),
      },
      //editor: this.editorial ? this.editorial.author : this.$store.state.auth.user
    }
  },

  methods: {
    saveEditorial() {
      // this.$emit('save', {
      //   type: 'article',
      //   title: this.title,
      //    content: this.content,
      // })
    }
  }

}
</script>
<style lang="sass">
@import './styles/components/article-perex'

//- Editorial Post Editor
.editorial-post-editor
  display: flex
  height: 100%

  > article
    display: flex
    flex-direction: column
    width: 100%

    background: #f5f5f5

    header section .save
      margin-left: auto

//- Content
.editorial-post-editor--content
  display: flex
  flex-direction: column
  flex: 1

  //- title
  > input
    margin-bottom: $baseline / 2
    padding: 0

    border: 0
    background: #f5f5f5

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600
    line-height: 1.58


  //- medium editor
  .medium-editor-wrapper
    flex: 1
    min-height: $baseline * 3

    background: #f5f5f5

    line-height: 1.58
    hyphens: auto

    +article-perex

    .ck-content
      height: 100%

</style>
