<template>
  <div class="myauthors-view">
    <template>
      <div
        v-if="!subscriptionExists"
        class="my-authors--empty"
      >
        <h1>{{ $t('No subscribed authors') }}</h1>
        <p>{{ $t('You haven\'t subscribed to any authors yet.') }}</p>

        <section>
          <h3>{{ $t('Explore interesting content') }}</h3>

          <ul>
            <li>{{ $t('Go to Explore page.') }}</li>
            <li>{{ $t('Subscribe newsletters or authors that caught your interest.') }}</li>
          </ul>
          <nuxt-link to="/explore">{{ $t('Explore authors') }}</nuxt-link>
        </section>
        <section>
          <h3>{{ $t('Import RSS feeds') }}</h3>
          <ul>
            <li>{{ $t('Add RSS/Atom source.') }}</li>
            <li>{{ $t('Or import OPML file with feeds.') }}</li>
          </ul>
          <nuxt-link to="/import">{{ $t('Import RSS') }}</nuxt-link>
        </section>
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
import AuthorWidget from '@/components/widgets/AuthorWidget'

function sortAuthors (a, b) {
  const aName = a.name.toLowerCase(); const bName = b.name.toLowerCase()
  return aName < bName ? -1 : (aName > bName ? 1 : 0)
}

export default {
  name: 'MyAuthors',

  components: {
    AuthorWidget
  },

  async fetch ({ store }) {
    await store.dispatch('getSubscriptions')
  },

  computed: {
    subscriptions () {
      const { authors } = this.$store.state.subscriptions
      return Object.values(authors).map(s => {
        return {
          ...s,
          author: this.$store.getters['entities/denormalize'](s.author, 'Author'),
        }
      })
    },

    subscriptionExists () {
      return this.subscriptions.length > 0
    },

    sections () {
      const sections = {
        suspended: [],
        '6x_per_day': [],
        '3x_per_day': [],
        daily: [],
        weekly: []
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

  head () {
    return {
      title: this.$t('Authors – My Subscription – Kairly')
    }
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

  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600
    text-align: center

  h1 + p
    margin-bottom: $baseline
    text-align: center

  section:first-of-type
    margin-bottom: $baseline

  h3
    margin-bottom: $baseline / 4
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

  h3 + p
    margin-bottom: auto

  ul,
  ol

    li
      list-style: disc outside
      margin-bottom: $baseline / 4
      margin-left: $baseline * 0.75

      line-height: 1.42

      a
        color: darken($c-base, 10%)

        font-weight: 600

        &:hover,
        &:focus
          color: darken($c-base, 20%)

  ol li
    list-style: decimal outside

  a
    +button(primary, small)

</style>
