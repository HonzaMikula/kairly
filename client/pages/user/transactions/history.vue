<template>
  <div class="transactions">
    <header>
      <h1>{{ $t('Credit balance') }}</h1>

      <nuxt-link to="/user/add-credits">
        <button>{{ $t('Buy credits') }}</button>
      </nuxt-link>
    </header>

    <section class="transactions--info">
      <div>
        <h3>{{ $t('Current balance') }}</h3>
        <p>{{ user.credits }} Kč</p>
      </div>

      <div>
        <h3>{{ $t('Monthly spending') }}</h3>
        <p>{{ monthSpending }} Kč</p>
      </div>
    </section>

    <h2>{{ $t('Transaction history') }}</h2>
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
  </div>
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

  computed: {
    ...mapState({
      user: state => state.auth.user,
    }),
    ...mapGetters(['monthSpending']),
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
//- Imports
@import './styles/components/buttons'

.transactions
  margin: $baseline auto
  padding: 0 $baseline/2
  max-width: 900px

  header
    display: flex
    margin-bottom: $baseline / 2

    //- heading
    > h1
      flex: 1

      font-size: $fs-3
      font-weight: 600

    //- add credit button
    button
      +button

  > h2
    margin-bottom: $baseline / 2

    font-size: $fs-3
    font-weight: 600

//- Info about balance
.transactions--info
  display: flex
  margin-bottom: $baseline

  div
    margin-right: $baseline

  h3
    font-weight: 600
    font-size: $fs-0



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
