<template>
  <post-component role="article" :class="post.type">
    <header v-on:mouseleave="closeAuthorWidget()">
      <picture>
        <router-link :to="{name: 'author', params: {author: post.author.id}}">
          <img :src="'http://kairly.com'+ post.author.picture" :alt="post.author.name" />
        </router-link>
      </picture>

      <h3>
        <router-link :to="{name: 'author', params: {author: post.author.id}}">
          {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </router-link>
      </h3>

      <authorPopup
        :author="post.author"
        v-if="isAuthorWidgetOpen"
        v-on:authorwidgetclose="closeAuthorWidget()">
      </authorPopup>

      <time>
        {{ post.time | moment('calendar') }}
      </time>

      <slot name="controls">
        <backlog-add :post="post" />
      </slot>
    </header>

    <slot></slot>
  </post-component>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import AuthorPopup from '@/components/widgets/AuthorPopup'
import BacklogAdd from '@/components/posts/BacklogAdd'

export default {
  name: 'post',
  props: ["post", "isSubscribed"],

  components: {
    AuthorPopup,
    BacklogAdd
  },

  directives: {
    onClickaway
  },

  data: function () {
    return {
      isAuthorWidgetOpen: false,
      isReadLaterWidgetOpen: false,
      isEditionWidgetOpen: false,
      timer: null,
    }
  },

  methods: {
    openAuthorWidget() {
      this.timer = setTimeout(() => {
        this.isAuthorWidgetOpen = true;
        this.$forceUpdate();
      }, 500);
    },

    closeAuthorWidget() {
      clearTimeout(this.timer)
      if (this.isAuthorWidgetOpen) {
        this.isAuthorWidgetOpen = false
        this.$forceUpdate()
      }
    }
  }
}
</script>

<style lang="sass">
//- Post -//
post-component
  display: block
  border-radius: 6px
  margin-bottom: $baseline / 2
  padding: $baseline / 2

  background: #fff

  &.tweet
    max-width: 576px

  @media (max-width: $mobile)
    padding: $baseline / 4


//- Post header
post-component > header
  position: relative

  display: grid
  grid-template-areas: "picture author" "picture info"
  grid-template-columns: 52px 1fr auto
  grid-template-rows: 0.75*$baseline 0.75*$baseline
  margin-bottom: $baseline / 2

  font-family: $ff-sans

  //-- author image
  picture
    grid-area: picture

    img
      border-radius: 100%
      height: $baseline * 1.5
      margin-right: $baseline / 2
      width: $baseline * 1.5

      object-fit: cover


  //-- author
  h3
    grid-area: author
    max-width: max-content

    color: $c-base

    font-size: $fs--2
    line-height: $baseline * 0.75

    a
      color: $c-base


  //-- date of publication
  time
    grid-area: info
    width: 100%

    color: #999

    font-size: $fs--2
    line-height: $baseline * 0.75

</style>
