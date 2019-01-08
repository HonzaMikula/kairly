<template>
  <app-layout :name="$t('Transactions')">
    <div class="transactions">
      <header>
        <h1>System Reports</h1>
      </header>

      Platform credits balance {{ credits }}

      <h2>Platform Transactions</h2>

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
      title: this.$t('System Reports')
    }
  },

  components: {
    AppLayout,
  },

  async fetch ({ store, redirect }) {
    if (!store.state.auth.user.isAdmin) {
      redirect('/')
      return
    }
  },

  async asyncData({ app, store, params }) {
    const { credits, transactions } = await app.$axios.$get(`/platform-transactions`)

    return {
      credits, transactions
    }
  },
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
