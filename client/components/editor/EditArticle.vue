<template>
  <div>
    <div class="edit-article--title">
      <input v-model="title" :placeholder="$t('Title')" />
    </div>

    <div class="edit-article--perex" :class="{'column-view': !normalPerexView}">
      <div class="edit-article--perex--controls">
        <button-icon
          class="normal-view"
          :class="{'is-active': normalPerexView}"
          @click="normalPerexView = true"
          tabindex="0"
          role="button">
          {{ $t('Normal view') }}
        </button-icon>

        <button-icon
          class="column-view"
          :class="{'is-active': !normalPerexView}"
          @click="normalPerexView = false"
          tabindex="0"
          role="button">
          {{ $t('Column view') }}
        </button-icon>
      </div>

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
      normalPerexView: true
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

//- Perex Controls
.edit-article--perex--controls
  margin-bottom: $baseline / 4

  button-icon
    display: inline-block
    border-radius: 3px
    height: $baseline * 1.25
    margin-right: $baseline / 4
    padding: 0 $baseline/4

    border: 1px solid #eee
    color: #777

    line-height: $baseline * 1.25

    &.is-active
      background: #fff
      color: #000


//- Perex
.edit-article--perex .medium-editor-wrapper
  line-height: 1.58
  hyphens: auto

  +article-perex

.edit-article--perex.column-view .medium-editor-wrapper
  column-count: 3
  column-rule: 1px dotted #ddd
  column-gap: $baseline

//- Content
.edit-article--content .medium-editor-wrapper
  +article-content


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

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
