<template>
  <div class="backlog-post">
    <header>
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

      <time>
        {{ post.time | moment('calendar') }}
        •
        {{ post.timeRead }} {{ $t('read') }}
        •
        <MoneyFormat :value="post.price" currency="Kč" />
      </time>

      <section>
        <button @click="$emit('publish')">{{ $t('Publish') }}</button>

        <button-icon
          class="remove"
          role="button"
          :title="$t('Remove post from considaration')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
          tabindex="0"
          @click.prevent="$emit('remove')">
        </button-icon>
      </section>

    </header>

    <template v-if="post.type == 'tweet'">
      <p v-html="post.content.content"></p>
    </template>

    <template v-else>
      <h2><nuxt-link :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link></h2>
    </template>
  </div>
</template>

<script>
import moment from 'moment'

import MoneyFormat from '@/components/widgets/MoneyFormat'

export default {
  name: 'BacklogPost',

  props: {
    post: Object,
    publish: Function,
    removePost: Function
  },

  components: {
    MoneyFormat
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- post
.backlog-post
  padding: $baseline / 4
  margin-bottom: $baseline / 2
  background: #fff

  //- article
  h2
    font-weight: 600
    font-family: $ff-serif

    word-break: break-word

    a
      color: #000

  //- tweet
  p
    font-family: $ff-serif

  > header
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
    section
      > button
        +button(primary, small)

      button-icon
        display: inline-block
        border-radius: 100%
        width: $baseline

        background: #eee

        text-align: center

        transition: 0.15s background

        &:focus,
        &:hover
          background: #ddd
</style>
