<template>
  <div>
    <div class="edit-article--title">
      <input
        v-model="title"
        :placeholder="$t('Title')"
      />
    </div>

    <div :class="{'edit-article--perex': true, 'column-view': !normalPerexView}">
      <div class="edit-article--perex--controls">
        <button-icon
          :class="{'normal-view': true, 'is-active': normalPerexView}"
          tabindex="0"
          role="button"
          @click="normalPerexView = true"
        >
          {{ $t('Normal view') }}
        </button-icon>

        <button-icon
          :class="{'column-view': true, 'is-active': !normalPerexView}"
          tabindex="0"
          role="button"
          @click="normalPerexView = false"
        >
          {{ $t('Column view') }}
        </button-icon>
      </div>

      <rich-editor
        v-model="perex"
        :options="perexOptions"
       />
    </div>

    <div class="edit-article--content">
      <rich-editor
        v-model="content"
        :options="contentOptions"
      />
    </div>

    <div class="edit-article--footer">
      <button @click="submit" :disabled="title === ''">{{ buttonTitle }}</button>
    </div>
  </div>
</template>


<script>
import { mapActions } from 'vuex'

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
        placeholder: 'Perex',
      },
      contentOptions: {
        placeholder: 'Content',
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
//- Imports
@import './styles/components/article-perex'
@import './styles/components/article-content'
@import './styles/components/buttons'

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

    .ck-content
      min-height: 260px


//- Footer
.edit-article--footer
  button
    +button(primary, large)

</style>
