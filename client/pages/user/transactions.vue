<template>
  <app-layout :name="$t('Transactions')">
    <div class="transactions">
      <header>
        <h1>Transaction history</h1>

        <button>Add credit</button>
      </header>

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
      title: this.$t('Account Settings – Kairly')
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
    > button
      +subscribed-button

      border-radius: $baseline * 0.625

      height: $baseline * 1.25

      line-height: $baseline * 1.25


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
