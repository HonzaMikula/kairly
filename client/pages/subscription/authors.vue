<template>
  <div>
    <template>
      <my-authors--empty
        v-if="authors.length === 0">
        <h1>No authors</h1>
        <p>You haven't subscribe to any author yet. On Explore page you can find authors you might like.</p>
        <nuxt-link to="/explore">Explore authors</nuxt-link>
      </my-authors--empty>

      <AuthorWidget
        v-for="author in authors"
        :key="author.slug"
        :author="author"
      />
    </template>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'MyAuthors',

  head: {
    title: 'My Subscription - Authors'
  },

  components: {
    AuthorWidget
  },

  computed: mapState({
    authors: state => {
      const subscriptions = state.subscriptions.authors
      const ids = Object.keys(subscriptions)
      const authors = ids.map(id => subscriptions[id].author)
      authors.sort(({title: a}, {title: b}) => a < b ? -1 : (a > b ? 1 : 0))
      return authors
    }
  }),

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }

    await store.dispatch('getSubscriptions')
  }
}
</script>

<style lang="sass">
my-newspapers-view author-widget-view
  width: 576px

my-authors--empty
  display: block
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  p
    margin-bottom: $baseline

  a
    +subscribed-button

    display: inline-block

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
