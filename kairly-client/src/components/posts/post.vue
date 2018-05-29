<template>
  <post-component role="article" :class="post.type">
    <header v-on:mouseleave="closeAuthorWidget()">
      <picture>
        <router-link :to="post.author.url">
          <img :src="post.author.picture" :alt="post.author.name" />
        </router-link>
      </picture>

      <h3>
        <router-link :to="post.author.url">
          {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </router-link>
      </h3>

      <authorWidget
        :author="post.author"
        v-if="isAuthorWidgetOpen"
        v-on:authorwidgetclose="closeAuthorWidget()">
      </authorWidget>

      <time>
        {{ post.time | moment('calendar') }}
      </time>
    </header>

    <slot></slot>
  </post-component>
</template>

<script>
import { directive as onClickaway } from 'vue-clickaway'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'post',
  props: ["post", "isSubscribed"],

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
  },

  components: {
    AuthorWidget
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
    width: 576px


//- Post header
post-component > header
  position: relative

  display: grid
  grid-template-areas: "picture author" "picture info"
  grid-template-columns: 52px auto
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

      text-decoration: none


  //-- date of publication
  time
    grid-area: info
    width: 100%

    color: #999

    font-size: $fs--2
    line-height: $baseline * 0.75

</style>
