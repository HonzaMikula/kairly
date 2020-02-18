<template>
  <article class="post"
    role="article"
    :class="post.type"
  >
    <header @mouseleave="closeAuthorWidget">
      <slot name="author">
        <picture>
          <template v-if="post.author.kind == 'external'">
            <a :href="post.author.url" target="_blank">
              <AuthorPicture :author="post.author" />
            </a>
          </template>
          <template v-else>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
              <AuthorPicture :author="post.author" />
            </nuxt-link>
          </template>
        </picture>

        <h3 :id="`post-author-${post.id}`">
          <template v-if="post.author.kind == 'external'">
            <a :href="post.author.url" target="_blank">{{ post.author.name }}</a>
          </template>
          <template v-else>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
              {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
            </nuxt-link>
          </template>
        </h3>

        <AuthorPopup
         v-if="post.author.kind != 'external'"
          :target="`post-author-${post.id}`"
          :author="post.author"
        />

        <time>{{ post.time | moment('MMM D') }}</time>
      </slot>

      <section>
        <slot name="global-controls"/>
        <slot name="page-controls">
          <span>
            <button
              v-if="user && post.author.id == user.id"
              class="edit"
              v-b-tooltip
              :title="$t('Edit post')"
              @click.prevent="$router.push(`/posts/${post.id}`)"
            />
            <button
              v-if="userNewspapers.length > 0 && post.type !== 'comment'"
              class="consider-post"
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
    <slot name="buttons"/>
  </article>
</template>

<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapState, mapGetters } from 'vuex'

import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorPopup from '@/components/widgets/AuthorPopup'
import ConsiderPost from '@/components/widgets/ConsiderPost'

export default {
  name: 'PostDetail',

  props: {
    post: Object,
  },

  components: {
    AuthorPicture,
    AuthorPopup,
    ConsiderPost,
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
    ...mapState({
      user: state => state.auth.user
    }),

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

  display: grid
  grid-template-columns: min-content minmax(auto, max-content) auto max-content
  align-items: center
  margin-bottom: $baseline / 4

  font-family: $ff-sans

  //-- author image
  picture img
    display: block
    border-radius: 100%
    height: $baseline
    margin-right: $baseline / 4
    width: $baseline

    object-fit: cover


  //-- author
  h3
    overflow: hidden

    color: #555

    font-size: $fs--1
    font-weight: 600
    white-space: nowrap
    text-overflow: ellipsis

    span
      font-weight: 400

    a
      color: #555


  //-- date of publication
  time
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

    span
      display: flex

    > a,
    > span > a,
    > button,
    > span > button,
    > button-icon,
    > span > button-icon
      margin-left: $baseline / 4

      background: #eee

      transition: 0.15s background

      &:hover,
      &:focus
        background: #ddd

      &.tweet
        +button-icon($fa-var-twitter, icon, brand, small)

      &.external-link::before
        +button-icon($fa-var-external-link-square-alt, icon, solid, small)

      &.edit
        +button-icon($fa-var-pencil-alt, icon, solid, small)

      &.up
        +button-icon($fa-var-arrow-up, icon, solid, small)

      &.down
        +button-icon($fa-var-arrow-down, icon, solid, small)

      &.remove
        +button-icon($fa-var-times, icon, solid, small)

      &.add
        +button-icon($fa-var-plus, icon, solid, small)

        background: $c-base
        color: #fff

        &:hover,
        &:focus
          background: darken($c-base, 10%)

      &.editorial
        +button-icon($fa-var-comment-dots, icon, solid, small)

        &.is-active
          background: $c-base

    button
      +button(primary, small)
      margin-left: $baseline / 4

    //- consider post
    > span
      position: relative

    //- price
    > .price
      margin-left: $baseline / 4
      margin-right: $baseline / 4

      font-weight: 600
      line-height: $baseline

    .consider-post
      +button-icon($fa-var-newspaper)

      height: $baseline
      width: $baseline

      &::before
        font-size: $fs--1
        line-height: $baseline


//- Popover TODO: maybe move it somewhere else
.popover-body
  padding: 0

  font-family: $ff-sans
  font-size: $fs-0

  li
    padding: $baseline/4 $baseline/2

    border-bottom: 1px solid #eee

    cursor: pointer

    &:last-of-type
      border-bottom: 0

    &:hover,
    &:focus
      background: #eee

    h6
      font-weight: 600

    p
      font-size: $fs--1
</style>
