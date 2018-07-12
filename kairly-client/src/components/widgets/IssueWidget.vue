<template>
  <issue-widget-view>
    <picture>
      <router-link :to="{name: 'issue', params: {author: issue.edition.editor.id, issue: issue.edition.name}}">
        <img :src="issue.edition.picture" :alt="issue.edition.title" />
      </router-link>
    </picture>

    <h2>
      <router-link :to="{name: 'issue', params: {author: issue.edition.editor.id, issue: issue.edition.name}}">{{ issue.edition.title }} #{{ issue.number }}</router-link>
    </h2>

    <issue-widget--author>
      <img :src="issue.edition.editor.picture" :alt="issue.edition.editor.name"/>
      <router-link :to="{name: 'author', params: {author: issue.edition.editor.id}}">{{ issue.edition.editor.name }}</router-link>
    </issue-widget--author>

    <ul>
      <li><a href="">Vláda posvětila přesun brněnského nádraží k Řece</a></li>
      <li><a href="">Babiš, už mě nebabiš. Sice postavil "psí boudu", ale vládu neumí, neumí, neumí</a></li>
      <li><a href="">ANO podepsalo koaliční smlouvu s ČSSD, i dohodu o toleranci s KSČM</a></li>
    </ul>

    <issue-widget--subscribe>
      <button
        v-bind:class="{ 'is-subscribed': issue.edition.subscription }"
        v-on:click="subscribe($event)"
      >{{ issue.edition.subscription ? 'Subscribed' : 'Subscribe'}}</button>
      <p>
        10 CZK per month
         •
        {{ issue.edition.likes }} subscribers
      </p>
    </issue-widget--subscribe>

  </issue-widget-view>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'IssueWidget',
  props: ['issue'],

  methods: {
    subscribe(ev) {
      const value = !this.issue.edition.subscription
      this.$store.dispatch('subscribe', {
        edition: this.issue.edition,
        value
      })
      ev.target.blur()
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

  //- button
  button
    +subscribe-button

    font-family: $ff-sans
    font-size: $fs--1

  //- info
  p
    font-size: $fs--2
</style>
