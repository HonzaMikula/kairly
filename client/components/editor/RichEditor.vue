<template>
  <!--div class="medium-editor-wrapper" ref="element" /-->
  <div class="medium-editor-wrapper">
    <ckeditor
      :editor="editor"
      :value="value"
      :config="editorConfig"
      @input="ev => $emit('input', ev)"
    />
  </div>
</template>

<script>
import CKEditor from '@ckeditor/ckeditor5-vue'
import BalloonBlockEditor from '@ckeditor/ckeditor5-build-balloon-block'
// import BalloonBlockEditor from 'ckeditor-build-kairly'

// const defaultOptions = {
//   toolbar: {
//     buttons: [
//       "bold", "italic", "underline", "anchor",  "h2", "h3", "h4", "quote",
//       "unorderedlist", "orderedlist"
//     ]
//   }
// }

const defaultOptions = {}

export default {
  name: 'RichEditor',

  components: {
    ckeditor: CKEditor.component
  },

  props: {
    value: [String],
    options: {
      type: [Object],
      default: () => {}
    }
  },

  data () {
    return {
      editor: BalloonBlockEditor,
      // content: this.value,
      editorConfig: { ...defaultOptions, ...this.options },
      content: '',
      // editorConfig: {}
    }
  }
}
</script>

<style lang="sass">
.medium-editor-wrapper
  box-sizing: border-box
  width: 100%
  background-color: white
  border: 0

  font-family: $ff-serif
  font-size: $fs-0
  line-height: 1.58

  .ck-content
    height: 100%

.medium-editor-placeholder::after
  font-style: normal

.medium-editor-toolbar li button.medium-editor-button-active
  background: $c-green
  color: white

.ck-block-toolbar-button
  border-radius: 100% !important
  background: #fff !important

  cursor: pointer !important
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff !important

  &:focus,
  &:hover
    background: #eee !important
</style>
