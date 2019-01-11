<template>
  <post-component role="article" :class="post.type">
    <header @mouseleave="closeAuthorWidget()">
      <picture>
        <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
          <img :src="post.author.picture" :alt="post.author.name" />
        </nuxt-link>
      </picture>

      <h3>
        <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
          {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </nuxt-link>
      </h3>

      <authorPopup
        :author="post.author"
        v-if="isAuthorWidgetOpen"
        @authorwidgetclose="closeAuthorWidget()">
      </authorPopup>

      <time>
        {{ post.time | moment('calendar') }}
      </time>

      <section>
        <slot name="extendedControls"></slot>
        <slot name="controls">
          <span>
            <button
              role="button"
              tabindex="0"
              class="consider-post"
              @click.stop.prevent="showConsiderPost = true"
              :aria-label="$t('Consider for newspaper')">
            </button>
            <consider-post v-if="showConsiderPost" :post="post" @closeConsiderPostDialog="closeConsiderPost" />
          </span>
        </slot>
      </section>

    </header>

    <slot></slot>

    <slot name="buttons"></slot>
  </post-component>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import AuthorPopup from '@/components/widgets/AuthorPopup'
import ConsiderPost from '@/components/widgets/ConsiderPost'

export default {
  name: 'PostDetail',
  props: ["post", "isSubscribed"],

  components: {
    AuthorPopup,
    ConsiderPost
  },

  directives: {
    onClickaway
  },

  data: function () {
    return {
      isAuthorWidgetOpen: false,
      timer: null,
      showConsiderPost: false
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
    },

    closeConsiderPost() {
      this.showConsiderPost = false
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

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

    font-size: $fs--1
    line-height: $baseline * 0.75

    a
      color: $c-base


  //-- date of publication
  time
    grid-area: info
    width: 100%

    color: #999

    font-size: $fs--1
    line-height: $baseline * 0.75

  //-- controls
  > section
    display: flex

    > *
      margin-left: $baseline / 4

    > button-icon,
    > a
      display: inline-block
      border-radius: 100%
      height: $baseline * 1.25
      width: $baseline * 1.25

      background: #eee
      color: #000

      cursor: pointer
      line-height: $baseline * 1.25
      text-align: center

      transition: 0.15s background

      &:focus,
      &:hover
        background: #ddd

    > a
      &::before
        +fa-icon()

      &.tweet::before
        @extend .fab
        content: fa-content($fa-var-twitter)

      &.external-link::before
        @extend .fas
        content: fa-content($fa-var-external-link-square-alt)

    > button
      +button(primary, medium)
      margin-left: $baseline / 4

    //- consider post
    > span
      position: relative

    .consider-post
      +button-icon($fa-var-newspaper)



</style>
