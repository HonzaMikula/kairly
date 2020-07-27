<template>
  <div class="my-newspapers-view">
    <div
      v-if="newspapers.length === 0"
      class="my-newspapers--empty"
    >
      <h1>{{ $t('No subscribed newsletters') }}</h1>
      <p>{{ $t('You haven\'t subscribed to any newsletters yet.') }}</p>

      <section>
        <h3>{{ $t('Explore interesting content') }}</h3>

        <ul>
          <li>{{ $t('Go to Explore page.') }}</li>
          <li>{{ $t('Subscribe newsletters or authors that caught your interest.') }}</li>
        </ul>
        <nuxt-link to="/explore">{{ $t('Explore newsletters') }}</nuxt-link>
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

    <template v-else>
      <NewspaperWidget
        v-for="newspaper in newspapers"
        :key="newspaper.fullName"
        :newspaper="newspaper"
      />
    </template>
  </div>
</template>

<script>
import NewspaperWidget from '@/components/widgets/NewspaperWidget'

export default {
  name: 'MyNewspapers',

  components: {
    NewspaperWidget
  },

  async asyncData ({ store }) {
    const { newspapers: subscriptions } = await store.dispatch('getSubscriptions')
    const newspapers = Object.keys(subscriptions).map(fullName => store.getters['entities/getNewspaper'](fullName))

    newspapers.sort(
      (a, b) => {
        const aSuspended = subscriptions[a.fullName].state === 'suspended'
        const bSuspended = subscriptions[b.fullName].state === 'suspended'
        if (aSuspended && !bSuspended) { return -1 }
        if (!aSuspended && bSuspended) { return 1 }
        const aTitle = a.title.toLowerCase()
        const bTitle = b.title.toLowerCase()
        return aTitle < bTitle ? -1 : (aTitle > bTitle ? 1 : 0)
      }
    )
    return { newspapers }
  },

  head () {
    return {
      title: this.$t('Newsletters – My Subscription – Kairly')
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.my-newspapers-view
  display: grid
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr
  grid-column-gap: $baseline / 2
  grid-row-gap: $baseline / 2

  @media (max-width: $mobile)
    grid-template-columns: 1fr 1fr
    grid-column-gap: $baseline / 4

.my-newspapers--empty
  grid-column: 1 / span 3

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
