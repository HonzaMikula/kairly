<template>
  <issue-widget-view>
    <picture>
      <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: issue.newspaper.editor.id, newspaper: issue.newspaper.name, issue: issue.number}}">
        <img v-if="issue.newspaper.picture" :src="issue.newspaper.picture" :alt="issue.newspaper.title" />
        <div v-else class="image-placeholder"></div>
      </nuxt-link>
    </picture>

    <h2>
      <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: issue.newspaper.editor.id, newspaper: issue.newspaper.name, issue: issue.number}}">{{ issue.newspaper.title }}</nuxt-link>
    </h2>

    <issue-widget--author>
      <img :src="issue.newspaper.editor.picture" :alt="issue.newspaper.editor.name"/>
      <nuxt-link :to="{name: 'author', params: {author: issue.newspaper.editor.id}}">{{ issue.newspaper.editor.name }}</nuxt-link>
    </issue-widget--author>

    <ul>
      <li v-for="post in issue.posts.slice(0, 3)" :key="post.id">
        <nuxt-link :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.type === 'tweet' ? `${post.author.name}'s tweet`  : post.content.title }}</nuxt-link>
      </li>
    </ul>

    <issue-widget--subscribe>
      <NewspaperSubscription :newspaper="issue.newspaper" />

      <p>
        {{ issue.newspaper.likes }} {{ $t('subscribers') }}
      </p>
    </issue-widget--subscribe>

  </issue-widget-view>
</template>

<script>
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'

export default {
  name: 'IssueWidget',

  props: {
    issue: Object
  },

  components: {
    NewspaperSubscription
  }
}
</script>

<style lang="sass">
issue-widget-view
  position: relative

  display: flex
  flex-direction: column
  flex: 1 0 270px
  padding: 0 $baseline / 4
  border-radius: $baseline / 4
  overflow: hidden

  background: #fff
  border: 1px solid #eee

  text-align: left

  //- header picture
  picture
    order: 1
    display: block
    margin: 0 (-$baseline)/4 0 (-$baseline)/4
    height: 120px

    img
      height: 100%
      width: 100%
      object-fit: cover

    .image-placeholder
      height: 100%
      background-image: radial-gradient(#fafafa, #aaa)

  //- title
  > h2
    order: 3
    font-weight: 600

    a
      color: #000

  //- list of posts
  ul
    flex: 1
    order: 4

    font-size: $fs--1
    line-height: $baseline * 0.8

    li
      margin-top: $baseline / 4

    a
      color: #555
      color: darken($c-base, 20%)

      &:focus,
      &:hover
        color: #000

//- Author + Periodicity
issue-widget--author
  font-size: $fs--1
  order: 2
  margin: $baseline/2 0

  img
    border-radius: 100%
    float: left
    height: $baseline
    margin-right: $baseline / 4
    width: $baseline

    object-fit: cover

  a
    color: #000


//- Subscribe issue
issue-widget--subscribe
  display: block
  padding: $baseline / 2 0 0 0
  order: 4

  text-align: center

  //- info
  p
    font-size: $fs--1
</style>
