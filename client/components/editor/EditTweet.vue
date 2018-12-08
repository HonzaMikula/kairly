<template>
  <div>
    <div class="edit-tweet--content">
      <textarea v-model="content" cols="80" rows="4" maxlength="320" :placeholder="$t('Tweet Content')" />
    </div>

    <div class="edit-tweet--footer">
      <button @click="submit">{{ buttonTitle }}</button>
    </div>
  </div>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

function htmlDecode(input){
  var e = document.createElement('div');
  e.innerHTML = input;
  // handle case of empty input
  return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

export default {
  name: 'EditTweet',

  props: {
    post: Object,
    buttonTitle: String
  },

  data() {
    return {
      content: this.post ? htmlDecode(this.post.content.content) : ''
    }
  },

  methods: {
    submit() {
      this.$emit('submit', {
        type: 'tweet',
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
.edit-tweet--footer
  button
    +subscribed-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5


</style>
