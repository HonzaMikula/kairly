<template>
  <my-editions--item>
    <picture>
      <img :src="edition.picture" :alt="edition.title" />
    </picture>

    <h2>{{ edition.title }}</h2>

    <p>{{ edition.description }}</p>

    <my-editions--item--author>
      <img :src="edition.editor.picture" :alt="edition.editor.name"/>
      {{ edition.editor.name }}
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
      this.$store.dispatch('subscribe', {
        edition: this.edition,
        value: !this.edition.isSubscribed
      })
      ev.target.blur()
    }
  }
}
</script>
