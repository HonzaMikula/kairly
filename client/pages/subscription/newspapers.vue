<template>
  <my-newspapers-view>
    <my-newspapers--empty
      v-if="newspapers.length === 0">
      <h1>No newspapers</h1>
      <p>You haven't subscribe to any newspapers yet. On Explore page you can find newspapers you might like.</p>
      <nuxt-link to="/explore">Explore newspapers</nuxt-link>
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
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'

export default {
  name: 'MyNewspapers',

  head: {
    title: 'Newspapers - My Subscription - Kairly'
  },

  components: {
    NewspaperWidget
  },

  computed: {
    ...mapState({
      newspaperIds: state => Object.keys(state.subscriptions.newspapers)
    }),

    newspapers() {
      const newspapers = this.newspaperIds
        .map(id => this.$store.getters.newspaper(id))
        .filter(newspaper => newspaper !== undefined)
      newspapers.sort(({title: a}, {title: b}) => a < b ? -1 : (a > b ? 1 : 0))
      return newspapers
    }
  },

  created() {
    this.$store.dispatch('getNewspapers', this.newspaperIds)
  }
}
</script>

<style lang="sass">
my-newspapers-view
  display: grid
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr 1fr
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
    +subscribed-button

    display: inline-block

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
