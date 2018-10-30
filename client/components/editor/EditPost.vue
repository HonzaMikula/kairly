<template>
  <div class="edit-post-view">

    <nav>
      <a href="" class="nuxt-link-active">Write an article</a>
      <a href="">Write a tweet</a>
    </nav>

    <div class="edit-post--title">
      <input v-model="title" placeholder="Title" />
    </div>

    <div class="edit-post--perex">
      <textarea v-model="perex" cols="80" rows="10" placeholder="Perex"/><br/>
    </div>

    <div class="edit-post--content">
      <textarea v-model="content" cols="80" rows="16" placeholder="Content" />
    </div>

    <div class="edit-post--footer">
      <button @click="submit">{{ buttonTitle }}</button>
    </div>
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
//- Switcher
.edit-post-view
  box-sizing: border-box
  padding: $baseline 0
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: $baseline $baseline/4

  nav
    margin-bottom: $baseline

    font-size: $fs-3

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 600

      &.nuxt-link-active
        color: #000

//- Title
.edit-post--title
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
.edit-post--perex,
.edit-post--content
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
.edit-post--footer
  button
    +subscribed-button
</style>
