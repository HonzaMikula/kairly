<template>
  <div class="myauthors-view">
    <template>
      <my-authors--empty
        v-if="!subscriptionExists">
        <h1>{{ $t('No authors') }}</h1>
        <p>{{ $t("You haven't subscribe to any author yet. On Explore page you can find authors you might like.") }}</p>
        <nuxt-link to="/explore">{{ $t('Explore authors') }}</nuxt-link>
      </my-authors--empty>

      <template v-if="authors['suspended'].length">
        <h2>{{ $t('Suspended') }}</h2>
        <AuthorWidget
          v-for="author in authors['suspended']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['6x_per_day'].length">
        <h2>{{ $t('Every 3 hours') }}</h2>
        <AuthorWidget
          v-for="author in authors['6x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['3x_per_day'].length">
        <h2>{{ $t('3x per day') }}</h2>
        <AuthorWidget
          v-for="author in authors['3x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['daily'].length">
        <h2>{{ $t('Daily') }}</h2>
        <AuthorWidget
          v-for="author in authors['daily']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="authors['weekly'].length">
        <h2>{{ $t('Weekly') }}</h2>
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

function sortByAuthorName(a, b) {
  const aName = a.author.name.toLowerCase(), bName = b.author.name.toLowerCase()
  return aName < bName ? -1 : (aName > bName ? 1 : 0)
}

export default {
  name: 'MyAuthors',

  head() {
    return {
      title: this.$t('Authors – My Subscription – Kairly')
    }
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
        'suspended': [],
        '6x_per_day': [],
        '3x_per_day': [],
        'daily': [],
        'weekly': []
      }
      Object.keys(subscriptions).forEach(id => {
        const subscription = subscriptions[id]
        if (subscription.state === 'suspended') {
          sections.suspended.push(subscription)
        } else {
          sections[subscription.periodicity.frequency].push(subscription)
        }
      })

      Object.keys(sections).forEach(key => {
          sections[key].sort(sortByAuthorName)
          sections[key] = sections[key].map(s => s.author)
      })

      return sections
    }
  }),

  async fetch({ store, redirect }) {
    await store.dispatch('getSubscriptions')
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.myauthors-view
  h2
    margin: $baseline 0 $baseline / 2

    font-family: $ff-sans
    font-size: $fs-1
    font-weight: 600

    &:first-of-type
      margin-top: 0

my-newspapers-view .author-widget-view
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
    +button(primary, large)

</style>
