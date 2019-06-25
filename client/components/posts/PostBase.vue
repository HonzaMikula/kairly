<template>
  <article class="post"
    role="article"
    :class="post.type"
  >
    <header @mouseleave="closeAuthorWidget">
      <slot name="author">
        <picture>
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
            <img
              :src="post.author.picture"
              :alt="post.author.name"
            />
          </nuxt-link>
        </picture>

        <h3>
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
            {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
          </nuxt-link>
        </h3>

        <AuthorPopup
          v-if="isAuthorWidgetOpen"
          :author="post.author"
          @authorwidgetclose="closeAuthorWidget"
        />

        <time>{{ post.time | moment('MMM D') }}</time>
      </slot>

      <section>
        <slot name="extendedControls"></slot>
        <slot name="controls">
          <span>
            <button
              v-if="userNewspapers.length > 0"
              class="consider-post"
              role="button"
              tabindex="0"
              :aria-label="$t('Consider for newspaper')"
              v-b-tooltip
              :title="$t('Consider for newspaper')"
              @click.stop.prevent="showConsiderPost = true"
            />
            <ConsiderPost v-if="showConsiderPost" :post="post" @closeConsiderPostDialog="closeConsiderPost" />
          </span>
        </slot>
      </section>

    </header>

    <slot/>

    <slot name="buttons"></slot>
  </article>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapGetters } from 'vuex'

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

  computed: {
    ...mapGetters(['userNewspapers']),
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
.post
  display: block
  border-radius: 6px
  margin-bottom: $baseline / 2
  padding: $baseline / 2

  background: #fff

  &.tweet,
  &.link
    max-width: 576px

  @media (max-width: $mobile)
    padding: $baseline / 4


//- Post header
.post > header
  position: relative

  display: flex
  align-items: center
  margin-bottom: $baseline / 4

  font-family: $ff-sans

  //-- author image
  picture
    grid-area: picture

    img
      display: block
      border-radius: 100%
      height: $baseline
      margin-right: $baseline / 4
      width: $baseline

      object-fit: cover


  //-- author
  h3
    grid-area: author
    max-width: max-content

    color: #555

    font-size: $fs--1
    font-weight: 600
    white-space: nowrap

    span
      font-weight: 400

    a
      color: #555


  //-- date of publication
  time
    flex: 1
    overflow: hidden

    color: #555

    font-size: $fs--1
    white-space: nowrap

    &::before
      margin: 0 $baseline/4
      content: '•'

  //-- controls
  > section
    display: flex

    > *
      margin-left: $baseline / 4

    > a,
    > button-icon
      border-radius: 100%
      height: $baseline * 1.25
      width: $baseline * 1.25

      line-height: $baseline * 1.25
      text-align: center

      background: #eee

      &:hover,
      &:focus
        background: #ddd

      &.tweet
        +button-icon($fa-var-twitter, icon, brand)

      &.external-link::before
        +button-icon($fa-var-external-link-square-alt, icon, solid)

    > button
      +button(primary, medium)
      margin-left: $baseline / 4

    //- consider post
    > span
      position: relative

    //- price
    > .price
      margin-right: $baseline / 4

      font-weight: 600
      line-height: $baseline * 1.25

    .consider-post
      +button-icon($fa-var-newspaper)

      height: $baseline
      width: $baseline

      &::before
        font-size: $fs--1
        line-height: $baseline



</style>
