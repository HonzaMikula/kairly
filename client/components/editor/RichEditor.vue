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
import CKEditor from '@ckeditor/ckeditor5-vue';
import BalloonEditor from '@ckeditor/ckeditor5-editor-balloon/src/ballooneditor';

import EssentialsPlugin from '@ckeditor/ckeditor5-essentials/src/essentials';
import BoldPlugin from '@ckeditor/ckeditor5-basic-styles/src/bold';
import ItalicPlugin from '@ckeditor/ckeditor5-basic-styles/src/italic';
import LinkPlugin from '@ckeditor/ckeditor5-link/src/link';
import ParagraphPlugin from '@ckeditor/ckeditor5-paragraph/src/paragraph';
//import Base64UploadAdapter from '@ckeditor/ckeditor5-upload/src/adapters/base64uploadadapter';

// const defaultOptions = {
//   toolbar: {
//     buttons: [
//       "bold", "italic", "underline", "anchor",  "h2", "h3", "h4", "quote",
//       "unorderedlist", "orderedlist"
//     ]
//   }
// }

const defaultOptions = {
  plugins: [
    EssentialsPlugin,
    BoldPlugin,
    ItalicPlugin,
    LinkPlugin,
    ParagraphPlugin
    //Base64UploadAdapter
  ],

  toolbar: {
    items: [
        'bold',
        'italic',
        'link',
        'undo',
        'redo'
    ]
  }
}

export default {
  name: 'rich-editor',

  props: {
    value: [String],
    options: {
      type: [Object],
      default: () => {}
    }
  },

  components: {
    ckeditor: CKEditor.component
  },

  data() {
    return {
      editor: BalloonEditor,
      //content: this.value,
      editorConfig: {...defaultOptions, ...this.options},
      content: '',
      //editorConfig: {}
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


.medium-editor-placeholder::after
  font-style: normal

.medium-editor-toolbar li button.medium-editor-button-active
  background: $c-green
  color: white
</style>
