<template>
  <app-layout :name="$t('Transactions')">
    <div class="transactions">
      <section>
        <header>
          <h1>Credit balance</h1>

          <nuxt-link to="/user/add-credits">
            <button>Add credit</button>
          </nuxt-link>
        </header>

      </section>

      <h2>Transaction history</h2>
      <table class="transactions--table">
        <thead>
          <tr>
            <th>Datetime</th>
            <th>Credits</th>
            <th>From ... To</th>
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
  </app-layout>
</template>

<script>
import { mapState, mapMutations } from 'vuex'


import AppLayout from '@/components/layout/AppLayout'


export default {
  name: 'Settings',

  head() {
    return {
      title: this.$t('Credit balance – Kairly')
    }
  },

  components: {
    AppLayout,
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

.transactions
  margin: $baseline auto
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
      +subscribed-button

      border-radius: $baseline * 0.625

      height: $baseline * 1.25

      line-height: $baseline * 1.25

  h2
    margin-bottom: $baseline / 2

    font-size: $fs-3
    font-weight: 600

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
