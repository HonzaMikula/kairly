<template>
  <div>
    <div class="edit-tweet--content">
      <textarea v-model="content" cols="80" rows="4" maxlength="320" placeholder="Tweet Content" />
    </div>

    <div class="edit-tweet--footer">
      <button @click="submit">{{ buttonTitle }}</button>
    </div>
  </div>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'EditTweet',

  props: {
    post: Object,
    buttonTitle: String
  },

  data() {
    return {
      content: this.post ? this.post.content.content : ''
    }
  },

  methods: {
    submit() {
      this.$emit('submit', {
        kind: 'tweet',
        content: this.content
      })
    }
  }
}
</script>

<style lang="sass">
//- Content
.edit-tweet--content
  margin-bottom: $baseline / 2

  textarea
    box-sizing: border-box
    padding: $baseline/4
    width: 100%
    border: 0
    font-family: $ff-serif
    font-size: $fs-0
    line-height: 1.58

//- Footer
.edit-article--footer
  button
    +subscribed-button

</style>
