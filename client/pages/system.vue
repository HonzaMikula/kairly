<template>
  <AppLayout :name="$t('Transactions')">
    <div class="transactions">
      <header>
        <h1>System Reports</h1>
      </header>

      <section class="system-transactions--balance">
        Platform credits balance <strong>{{ credits }}</strong> Kč
      </section>

      <h2>Platform Transactions</h2>

      <table class="system-transactions--table">
        <thead>
          <tr>
            <th>Datetime</th>
            <th>Credits</th>
            <th>From</th>
            <th>To</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transactions" :key="t.created">
            <td>{{ t.created | moment('calendar') }}</td>
            <td>
              <MoneyFormat :value="t.credits" currency="Kč" :force-sign="true"/>
            </td>

            <td v-if="t.source.newspaper">
              <!-- Monthly reward for newspaper editor -->
              <img :src="t.source.newspaper.picture" :alt="t.source.newspaper.name" />
              {{ t.source.newspaper.name}}
            </td>
            <td v-else-if="t.source.author">
              <!-- Monthly reward for author -->
              <img :src="t.source.author.picture" :alt="t.source.author.name" />
              {{ t.source.author.name }}
            </td>
            <td v-else>System</td>

            <td v-if="t.target.user">
              <!-- Monthly reward for author -->
              <img v-if="t.target.user.picture" :src="t.target.user.picture" :alt="t.target.user.name" />
              {{ t.target.user.name }}
            </td>
            <td v-else>System</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import MoneyFormat from '@/components/widgets/MoneyFormat'


export default {
  name: 'Settings',

  head() {
    return {
      title: this.$t('System Reports')
    }
  },

  components: {
    AppLayout,
    MoneyFormat
  },

  async fetch ({ store, redirect }) {
    if (!store.state.auth.user.isAdmin) {
      redirect('/')
      return
    }
  },

  async asyncData({ store, params }) {
    const { credits, transactions } = await store.dispatch(`getPlatformTransactions`)
    return { credits, transactions }
  },
}
</script>

<style lang="sass">
.system-transactions--balance
  margin-bottom: $baseline

  font-size: $fs-1


.system-transactions--table
  width: 100%

  a
    color: #000

  thead th
    padding: $baseline/4

    background: #eee

    font-weight: 600
    text-align: left

  tbody th,
  tbody td
    padding: $baseline / 4

    border-bottom: 1px solid #eee

    line-height: $baseline * 1.25

    img
      float: left
      height: $baseline * 1.25
      margin-right: $baseline / 4
      width: $baseline * 1.25

      object-fit: cover

  td.author img
    border-radius: 100%

</style>
