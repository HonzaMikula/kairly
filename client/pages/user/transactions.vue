<template>
  <app-layout :name="$t('Transactions')">
    <div style="width: 600px; margin: 0 auto">
      <table class="transactions-table">
        <tr>
          <th>Datetime</th>
          <th>Credits</th>
          <th>From ... To</th>
        </tr>
        <tr v-for="t in transactions">
          <td>{{ t.created | moment('calendar') }}</td>
          <td>{{ t.credits > 0 ? '+' : ''}}{{ t.credits }}</td>
          <td>{{ t.source }} ... {{ t.target }}</td>
        </tr>
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
.transactions-table
  margin-top: 20px
  width: 100%

  th
    background-color: #eee
  td
    padding: 3px 6px

</style>
