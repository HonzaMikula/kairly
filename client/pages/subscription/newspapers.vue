<template>
  <my-newspapers-view>
    <my-newspapers--empty
      v-if="newspapers.length === 0">
      <h1>{{ $t('No newspapers') }}</h1>
      <p>{{ $t('You haven\'t subscribe to any newspapers yet. On Explore page you can find newspapers you might like.') }}</p>
      <nuxt-link to="/explore">{{ $t('Explore newspapers') }}</nuxt-link>
    </my-newspapers--empty>

    <NewspaperWidget
      v-else
      v-for="newspaper in newspapers"
      :key="newspaper.fullName"
      :newspaper="newspaper"
    />
  </my-newspapers-view>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'

export default {
  name: 'MyNewspapers',

  head() {
    return {
      title: this.$t('Newspapers – My Subscription – Kairly')
    }
  },

  components: {
    NewspaperWidget
  },

  async asyncData({ store }) {
    const {newspapers: newspaperSubscriptions} = await store.dispatch('getSubscriptions')
    const newspapers = await store.dispatch('getNewspapers', Object.keys(newspaperSubscriptions))
    newspapers.sort(
      (a, b) => {
        const aSuspended = newspaperSubscriptions[a.fullName].state === 'suspended'
        const bSuspended = newspaperSubscriptions[b.fullName].state === 'suspended'
        if (aSuspended && !bSuspended) return -1
        if (!aSuspended && bSuspended) return 1
        const aTitle = a.title.toLowerCase()
        const bTitle = b.title.toLowerCase()
        return aTitle < bTitle ? -1 : (aTitle > bTitle ? 1 : 0)
      }
    )
    return {
      newspapers
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

my-newspapers-view
  display: grid
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr
  grid-column-gap: $baseline / 2
  grid-row-gap: $baseline / 2

  @media (max-width: $mobile)
    grid-template-columns: 1fr 1fr
    grid-column-gap: $baseline / 4

my-newspapers--empty
  grid-column: 1 / span 3

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
