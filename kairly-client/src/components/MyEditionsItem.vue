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
