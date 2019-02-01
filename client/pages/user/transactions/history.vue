<template>
  <table class="transactions--table">
    <thead>
      <tr>
        <th>{{ $t('Subject') }}</th>
        <th>{{ $t('Datetime') }}</th>
        <th>{{ $t('Credits') }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="t in transactions" :key="t.created">
        <td v-if="t.target.newspaper" class="newspaper">
            <!-- Newspaper subscription -->
            <nuxt-link :to="{name: 'author-newspaper', params: {author: t.target.newspaper.editor.id, newspaper: t.target.newspaper.name}}">
              <img :src="t.target.newspaper.picture" :alt="t.target.newspaper.name" />
              {{ t.target.newspaper.title}}
              <template v-if="t.kind === 'DO'"> – donation</template>
            </nuxt-link>
        </td>

        <td v-if="t.source.newspaper">
          <!-- Monthly reward for newspaper editor -->
          <nuxt-link :to="{name: 'author-newspaper', params: {author: t.source.newspaper.editor.id, newspaper: t.source.newspaper.name}}">
            <img :src="t.source.newspaper.picture" :alt="t.source.newspaper.name" />
            {{ t.source.newspaper.title}}
          </nuxt-link>
        </td>

        <td v-else-if="t.target.author" class="author">
          <!-- Author subscription -->
          <nuxt-link :to="{name: 'author', params: {author: t.target.author.id}}">
            <img :src="t.target.author.picture" :alt="t.target.author.name" />
            {{ t.target.author.name }}
            <template v-if="t.kind === 'DO'"> – donation</template>
          </nuxt-link>
        </td>

        <td v-else-if="t.source.author">
          <!-- Monthly reward for author -->
          Income from subscriptions
        </td>

        <td v-else-if="t.kind === 'FC'">
          Free credits
        </td>
        <td>{{ fmtTime(t.created) }}</td>
        <td>{{ t.credits > 0 ? '+' : ''}}{{ t.credits }} Kč</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import moment from 'moment'

import { mapState, mapGetters } from 'vuex'

export default {
  name: 'TransactionHistory',

  head() {
    return {
      title: this.$t('Credit balance – Kairly')
    }
  },

  methods: {
    fmtTime(datetime) {
      const format = this.$i18n.locale === 'cs' ? 'D.M.YYYY HH:mm' : 'M/D/YYYY HH:mm'
      return moment(datetime).format(format)
    }
  },

  async fetch({ store }) {
    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }
  },

  async asyncData({ app, store, params }) {
    const transactions = await store.dispatch('getTransactions')

    return {
      transactions
    }
  }
}
</script>

<style lang="sass">
.transactions--table
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
