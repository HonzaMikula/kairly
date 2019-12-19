<template>
  <div class="myauthors-view">
    <template>
      <div class="my-authors--empty"
        v-if="!subscriptionExists">
        <h1>{{ $t('No authors') }}</h1>
        <p>{{ $t("You haven't subscribe to any author yet. On Explore page you can find authors you might like.") }}</p>
        <nuxt-link to="/explore">{{ $t('Explore authors') }}</nuxt-link>
      </div>

      <template v-if="sections['suspended'].length">
        <h2>{{ $t('Suspended') }}</h2>
        <AuthorWidget
          v-for="author in sections['suspended']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="sections['6x_per_day'].length">
        <h2>{{ $t('Every 3 hours') }}</h2>
        <AuthorWidget
          v-for="author in sections['6x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="sections['3x_per_day'].length">
        <h2>{{ $t('3x per day') }}</h2>
        <AuthorWidget
          v-for="author in sections['3x_per_day']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="sections['daily'].length">
        <h2>{{ $t('Daily') }}</h2>
        <AuthorWidget
          v-for="author in sections['daily']"
          :key="author.slug"
          :author="author"
        />
      </template>

      <template v-if="sections['weekly'].length">
        <h2>{{ $t('Weekly') }}</h2>
        <AuthorWidget
          v-for="author in sections['weekly']"
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

function sortAuthors(a, b) {
  const aName = a.name.toLowerCase(), bName = b.name.toLowerCase()
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

  computed: {
    subscriptions() {
      const { authors } = this.$store.state.subscriptions
      return Object.values(authors).map(s => {
        return {
          ...s,
          author: this.$store.getters['entities/denormalize'](s.author, 'Author'),
        }
      })
    },

    subscriptionExists() {
      return this.subscriptions.length > 0
    },

    sections() {
      const sections = {
        'suspended': [],
        '6x_per_day': [],
        '3x_per_day': [],
        'daily': [],
        'weekly': []
      }
      this.subscriptions.forEach(subscription => {
        if (subscription.state === 'suspended') {
          sections.suspended.push(subscription)
        } else {
          sections[subscription.periodicity.frequency].push(subscription)
        }
      })

      Object.keys(sections).forEach(key => {
        sections[key] = sections[key].map(s => s.author)
        sections[key].sort(sortAuthors)
      })

      return sections
    }
  },

  async fetch({ store }) {
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

.my-newspapers-view .author-widget-view
  width: 576px

.my-authors--empty
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
