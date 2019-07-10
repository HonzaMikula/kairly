<template>
  <div class="backlog-post">
    <header>
      <picture>
        <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
          <img :src="post.author.picture" :alt="post.author.name" />
        </nuxt-link>
      </picture>

      <h3>
        <template v-if="post.author.kind == 'external'">
          <a :href="post.author.url" target="_blank">{{ post.author.name }}</a>
        </template>
        <template v-else>
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
            {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
          </nuxt-link>
        </template>
        •
        {{ post.time | moment('MMM D') }}
      </h3>

      <section>
        <button @click="$emit('publish')">{{ $t('Publish') }}</button>

        <button-icon
          class="remove"
          role="button"
          :title="$t('Remove post from considaration')"
          v-b-tooltip
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
      <p>
        {{ post.timeRead }} {{ $t('read') }}
        •
        <MoneyFormat :value="post.price" currency="Kč" />
      </p>
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
    grid-template-columns: min-content auto 1fr
    align-items: center
    margin-bottom: $baseline / 4

    font-family: $ff-sans

    //-- author image
    picture

      img
        display: block
        border-radius: 100%
        height: $baseline
        margin-right: $baseline / 4
        width: $baseline

        object-fit: cover


    //-- author
    h3
      color: #555

      font-size: $fs--1
      overflow: hidden
      white-space: nowrap
      text-overflow: ellipsis

      a
        color: #555

    //-- controls
    section
      display: flex
      justify-content: flex-end

      > button
        +button(primary, small)

        margin-right: $baseline / 4

      > button-icon
        background: #eee

        transition: 0.15s background

        &:focus,
        &:hover
          background: #ddd

        &.up
          +button-icon($fa-var-arrow-up, icon, solid, small)

        &.down
          +button-icon($fa-var-arrow-down, icon, solid, small)

        &.remove
          +button-icon($fa-var-times, icon, solid, small)
</style>
