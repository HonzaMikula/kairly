<template>
  <div>
    Title<br/>
    <input v-model="title" style="width: 100%"/><br/>

    Perex<br/>
    <textarea v-model="perex" cols="80" rows="10"/><br/>

    Content<br/>
    <textarea v-model="content" cols="80" rows="25" /><br/>


    <button @click="submit">{{ buttonTitle }}</button>
  </div>
</template>


<script>


import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'EditPosts',

  props: {
    post: Object,
    buttonTitle: String
  },

  data() {
    return {
      title: this.post ? this.post.content.title : '',
      perex: this.post ? this.post.content.perex : '',
      content: this.post ? this.post.content.content : '',
    }
  },

  methods: {
    submit() {
      this.$emit('submit', {
        title: this.title,
        perex: this.perex,
        content: this.content
      })
    }
  }
}
</script>

<style lang="sass">
</style>
