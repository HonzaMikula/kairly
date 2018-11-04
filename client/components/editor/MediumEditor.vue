<template>
  <div class="medium-editor-wrapper" ref="element">
  </div>
</template>

<script>
import MediumEditor from 'medium-editor'

const defaultOptions = {
  toolbar: {
    buttons: [
      "bold", "italic", "underline", "anchor",  "h2", "h3", "h4", "quote",
      "unorderedlist", "orderedlist"
    ]
  }
}

export default {
  name: 'medium-editor',
  props: {
    value: [String],
    options: {
      type: [Object],
      default: () => {}
    }
  },

  mounted (evt) {
    this.createAndSubscribe()
  },

  beforeDestroy (evt) {
    this.tearDown()
  },

  methods: {
    tearDown () {
      this.api.unsubscribe('editableInput', this.emit)
      this.api.destroy()
    },

    createAndSubscribe () {
      this.$refs.element.innerHTML = this.value

      this.api = new MediumEditor(this.$refs.element, {...defaultOptions, ...this.options})

      // bind edit operations to model
      // we need to store the handler in order to later on detach it again
      this.emit = event => {
        //this.$emit('edit', {event, api: this.api
        this.$emit('input', this.$refs.element.innerHTML)
      }
      this.api.subscribe('editableInput', this.emit)

      // emit event to give parent access to MediumEditor instance
      //this.$emit('editorCreated', this.api);
    }
  },
  watch: {
    value (newText) {
      // innerHTML MUST not be performed if the text did not actually change.
      // otherwise, the caret position will be reset.
      if (newText !== this.$refs.element.innerHTML) {
        this.api.setContent(this.value, 0)
        this.$refs.element.innerHTML = this.value
      }
    },
    /**
     * There is currently no way to change the options of a medium editor
     * without destroying and re-setting up the MediumEditor object.
     * We only tear down the editor, if the options actually changed.
     * See: https://github.com/yabwe/medium-editor/issues/1129
     */
    options (newOptions) {
      this.tearDown()
      this.createAndSubscribe()
    }
  },
  MediumEditor
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
