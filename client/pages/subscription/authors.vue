<template>
  <div class="myauthors-view">
    <template>
      <my-authors--empty
        v-if="!subscriptionExists">
        <h1>No authors</h1>
        <p>You haven't subscribe to any author yet. On Explore page you can find authors you might like.</p>
        <nuxt-link to="/explore">Explore authors</nuxt-link>
      </my-authors--empty>

      <template v-if="authors['6x_per_day'].length">
        <h2>6x per day</h2>
        <AuthorWidget
          v-for="author in authors['6x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['3x_per_day'].length">
        <h2>3x per day</h2>
        <AuthorWidget
          v-for="author in authors['3x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['daily'].length">
        <h2>Daily</h2>
        <AuthorWidget
          v-for="author in authors['daily']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['weekly'].length">
        <h2>Weekly</h2>
        <AuthorWidget
          v-for="author in authors['weekly']"
          :key="author.slug"
          :author="author"
        />
      </template>

    </template>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'MyAuthors',

  head: {
    title: 'My Subscription – Authors – Kairly'
  },

  components: {
    AuthorWidget
  },

  computed: mapState({
    subscriptionExists: state => {
      return Object.keys(state.subscriptions.authors).length > 0
    },

    authors: state => {
      const subscriptions = state.subscriptions.authors
      const sections = {
        '6x_per_day': [],
        '3x_per_day': [],
        'daily': [],
        'weekly': []
      }
      Object.keys(subscriptions).forEach(id => {
        const subscription = subscriptions[id]
        sections[subscription.periodicity.frequency].push(subscription)
      })
      sections['3x_per_day'].sort((a, b) => {
        const aName = a.author.name, bName = b.author.name
        return aName < bName ? -1 : (aName > bName ? 1 : 0)
      })
      sections['6x_per_day'].sort((a, b) => {
        const aName = a.author.name, bName = b.author.name
        return aName < bName ? -1 : (aName > bName ? 1 : 0)
      })
      sections['daily'].sort((a, b) => {
        const aTime = a.periodicity.time, bTime = b.periodicity.time
        const aName = a.author.name, bName = b.author.name
        if (aTime < bTime) return -1
        if (aTime > bTime) return 1
        return aName < bName ? -1 : (aName > bName ? 1 : 0)
      })
      sections['weekly'].sort((a, b) => {
        const aDow = a.periodicity.dow === 0 ? 7 : a.periodicity.dow
        const bDow = b.periodicity.dow === 0 ? 7 : b.periodicity.dow
        const aTime = a.periodicity.time, bTime = b.periodicity.time
        const aName = a.author.name, bName = b.author.name
        if (aDow < bDow) return -1
        if (aDow > bDow) return 1
        if (aTime < bTime) return -1
        if (aTime > bTime) return 1
        return aName < bName ? -1 : (aName > bName ? 1 : 0)
      })

      sections['6x_per_day'] = sections['6x_per_day'].map(s => s.author)
      sections['3x_per_day'] = sections['3x_per_day'].map(s => s.author)
      sections['daily'] = sections['daily'].map(s => s.author)
      sections['weekly'] = sections['weekly'].map(s => s.author)

      return sections
    }
  }),

  async fetch({ store, redirect }) {
    await store.dispatch('getSubscriptions')
  }
}
</script>

<style lang="sass">
.myauthors-view
  h2
    margin: $baseline 0 $baseline / 2

    font-family: $ff-sans
    font-size: $fs-2
    font-weight: 600

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
