<template>
  <issue-widget-view>
    <picture>
      <router-link :to="{name: 'issue', params: {author: issue.newspaper.editor.id, newspaper: issue.newspaper.name, issue: issue.number}}">
        <img :src="issue.newspaper.picture" :alt="issue.newspaper.title" />
      </router-link>
    </picture>

    <h2>
      <router-link :to="{name: 'issue', params: {author: issue.newspaper.editor.id, newspaper: issue.newspaper.name, issue: issue.number}}">{{ issue.newspaper.title }} #{{ issue.number }}</router-link>
    </h2>

    <issue-widget--author>
      <img :src="issue.newspaper.editor.picture" :alt="issue.newspaper.editor.name"/>
      <router-link :to="{name: 'author', params: {author: issue.newspaper.editor.id}}">{{ issue.newspaper.editor.name }}</router-link>
    </issue-widget--author>

    <ul>
      <li v-for="post in issue.posts" :key="post.id">
        <router-link :to="{ name: 'post', params: { postId: post.id }}">{{ post.type === 'tweet' ? `${post.author.name}'s tweet`  : post.content.title }}</router-link>
      </li>
    </ul>

    <issue-widget--subscribe>
      <button
        v-if="isSubscribed"
        class="is-subscribed"
        @click="unsubscribe($event)">
        <span class="default">Subscribed</span>
        <span class="on-hover">Unsubscribe</span>
      </button>

      <button
        v-else
        class="to-subscribe"
        @click="subscribe($event)">
        Subscribe
      </button>
      <p>
        10 CZK per month
         •
        {{ issue.newspaper.likes }} subscribers
      </p>
    </issue-widget--subscribe>

  </issue-widget-view>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'IssueWidget',

  props: {
    issue: Object
  },

  computed: {
    isSubscribed() {
      return this.issue.newspaper.fullName in this.$store.state.subscriptions.newspapers
    }
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', this.issue.newspaper.fullName)
      document.activeElement.blur()
    },

    unsubscribe(ev) {
      this.$store.dispatch('unsubscribe', this.issue.newspaper.fullName)
      document.activeElement.blur()
    }
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

  @media (max-width: $mobile)
    width: 260px

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

    font-size: $fs--2
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

  //- when newspaper is subscribed
  button.is-subscribed
    +subscribed-button

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when newspaper is ready to be subsribed
  button.to-subscribe
    +subscribe-button

    border-radius: $baseline * 0.5
    height: $baseline * 1
    width: 140px

    line-height: $baseline * 1

  //- info
  p
    font-size: $fs--2
</style>
