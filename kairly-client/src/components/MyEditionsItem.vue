<template>
  <my-editions--item>
    <picture>
      <router-link :to="'/editions/' + edition.id">
      <img :src="edition.picture" :alt="edition.title" />
      </router-link>
    </picture>

    <h2><router-link :to="'/editions/' + edition.id">{{ edition.title }}</router-link></h2>

    <p>{{ edition.description }}</p>

    <my-editions--item--author>
      <img :src="edition.editor.picture" :alt="edition.editor.name"/>
      <router-link :to="edition.editor.url">{{ edition.editor.name }}</router-link>
    </my-editions--item--author>

    <my-editions--item--subscribe>
      <button
        v-bind:class="{ 'is-subscribed': edition.isSubscribed }"
        v-on:click="subscribe($event)"
      >{{ edition.isSubscribed ? 'Subscribed' : 'Subscribe'}}</button>
      <p>
        10 CZK per month
         •
        {{ edition.likes }} subscribers
        •
        #{{ edition.issues }}
      </p>
    </my-editions--item--subscribe>

  </my-editions--item>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'MyEditionsItem',
  props: ['edition'],

  methods: {
    subscribe(ev) {
      const value = !this.edition.isSubscribed
      this.$store.dispatch('subscribe', {
        edition: this.edition,
        value
      })
      ev.target.blur()
    }
  }
}
</script>

<style lang="sass">
my-editions--item
  position: relative

  display: flex
  flex-direction: column
  flex: 1 0 270px
  padding: 0 $baseline / 4
  border-radius: $baseline / 4
  margin: 0 $baseline/4 $baseline $baseline/4
  overflow: hidden
  max-width: 280px

  background: #fff
  border: 1px solid #eee

  font-family: $ff-serif
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
    font-size: $fs-1
    font-weight: 600

    a
      color: #000

      text-decoration: none

  //- description
  > p
    flex: 1
    order: 4
    
    color: #777 

    font-size: $fs--1    
    line-height: $baseline * 0.8    

//- Author + Periodicity
my-editions--item--author

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

    text-decoration: none  
    

//- Subscribe Edition
my-editions--item--subscribe
  display: block
  padding: $baseline / 2 0 0 0
  order: 4

  text-align: center

  //- button
  button
    +subscribe-button

  //- info
  p
    font-size: $fs--2
</style>
