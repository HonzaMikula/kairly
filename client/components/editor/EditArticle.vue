<template>
  <div>
    <div class="edit-article--title">
      <input v-model="title" placeholder="Title" />
    </div>

    <div class="edit-article--perex">
      <medium-editor v-model="perex" :options="perexOptions" />
    </div>

    <div class="edit-article--content">
      <medium-editor v-model="content" :options="contentOptions" />
    </div>

    <div class="edit-article--footer">
      <button @click="submit">{{ buttonTitle }}</button>
    </div>
  </div>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'EditArticle',

  props: {
    post: Object,
    buttonTitle: String
  },

  data() {
    return {
      title: this.post ? this.post.content.title : '',
      perex: this.post ? this.post.content.perex : '',
      content: this.post ? this.post.content.content : '',
      perexOptions: {
        placeholder: {text: 'Perex', hideOnClick: false},
      },
      contentOptions: {
        placeholder: {text: 'Content', hideOnClick: false},
      },
    }
  },

  methods: {
    submit() {
      this.$emit('submit', {
        type: 'newspaper',
        title: this.title,
        perex: this.perex,
        content: this.content
      })
    }
  }
}
</script>

<style lang="sass">
//- Title
.edit-article--title
  margin-bottom: $baseline / 2

  input
    box-sizing: border-box
    height: $baseline * 1.5
    padding: 0 $baseline/4
    width: 100%

    border: 0

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600
    line-height: 1.58

//- Perex, Content
.edit-article--perex,
.edit-article--content
  margin-bottom: $baseline / 2

  .medium-editor-wrapper
    padding: $baseline/4
    width: 100%
    min-height: 260px


//- Footer
.edit-article--footer
  button
    +subscribed-button

</style>
