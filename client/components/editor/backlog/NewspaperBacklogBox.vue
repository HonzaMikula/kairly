<template>
  <div>
    {{ post }}
  </div>
</template>

<script>
export default {
  name: 'NewspaperBacklogPost',

  components: {
  },

  data() {
    return {
      editorType: null,
      editorPosition: null,
      mobileControls: false
    }
  },

  props: {
    newspaper: Object,
    post: Object,
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: String,
  }
}
</script>
