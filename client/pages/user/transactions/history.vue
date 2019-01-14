<template>
  <table class="transactions--table">
    <thead>
      <tr>
        <th>{{ $t('Datetime') }}</th>
        <th>{{ $t('Credits') }}</th>
        <th>{{ $t('From ... To') }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="t in transactions" :key="t.created">
        <td>{{ t.created | moment('calendar') }}</td>
        <td>{{ t.credits > 0 ? '+' : ''}}{{ t.credits }}</td>
        <td>{{ t.source }} ... {{ t.target }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'TransactionHistory',

  head() {
    return {
      title: this.$t('Credit balance – Kairly')
    }
  },

  async fetch({ store }) {
    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }
  },

  async asyncData({ app, store, params }) {
    const { credits, transactions } = await app.$axios.$get(`/transactions`)

    store.commit('updateCredits', credits)

    return {
      transactions
    }
  }
}
</script>

<style lang="sass">
.transactions--table
  width: 100%

  thead th
    padding: $baseline/4

    background: #eee

    font-weight: 600
    text-align: left

  tbody th,
  tbody td
    padding: $baseline/4

    border-bottom: 1px solid #eee

</style>
