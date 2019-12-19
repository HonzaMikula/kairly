<template>
  <table class="transactions--upcoming">
    <thead>
      <tr>
        <th>{{ $t('Newspaper / Author') }}</th>
        <th>{{ $t('Date of upcoming payment') }}</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(t, index) in transactions" :key="index">
        <template v-if="t.author">
          <td class="author">
            <nuxt-link :to="{name: 'author', params: {author: t.author.id}}">
              <img :src="t.author.picture" :alt="t.author.name" />
              {{ t.author.name }}
            </nuxt-link>
          </td>
          <td>{{ fmtTime(t.to) }}</td>
          <td><AuthorSubscriptionButton :author="t.author" /></td>
        </template>
        <template v-if="t.newspaper">
          <td class="newspaper">
            <nuxt-link :to="{name: 'author-newspaper', params: {author: t.newspaper.editor.id, newspaper: t.newspaper.name}}">
              <img :src="t.newspaper.picture" :alt="t.newspaper.name" />
              {{ t.newspaper.title}}
            </nuxt-link>
          </td>
          <td>{{ fmtTime(t.to) }}</td>
          <td>
            <NewspaperSubscriptionButton :newspaper="t.newspaper" />
          </td>
        </template>
      </tr>
    </tbody>
  </table>
</template>

<script>
import moment from 'moment'

import { sortBy } from '@/utils/array'

import AuthorSubscriptionButton from '@/components/widgets/AuthorSubscriptionButton'
import NewspaperSubscriptionButton from '@/components/widgets/NewspaperSubscriptionButton'

export default {
  name: 'UpcomingTransactions',

  head() {
    return {
      title: this.$t('Upcoming payments') + ' – Kairly'
    }
  },

  components: {
    AuthorSubscriptionButton,
    NewspaperSubscriptionButton,
  },

  computed: {
    authorSubscriptions() {
      const { authors } = this.$store.state.subscriptions
      return Object.values(authors).map(s => {
        return {
          ...s,
          author: this.$store.getters['entities/denormalize'](s.author, 'Author'),
        }
      })
    },

    newspaperSubscriptions() {
      const { newspapers } = this.$store.state.subscriptions
      return Object.entries(newspapers).map(([id, s]) => {
        return {
          ...s,
          newspaper: this.$store.getters['entities/denormalize'](id, 'Newspaper'),
        }
      })
    },

    transactions() {
      const { authors, newspapers } = this.$store.state.subscriptions
      const transactions = this.authorSubscriptions
        .filter(sub => {
          if (sub.state !== 'active') return false
          if (sub.donation !== null &&  parseFloat(sub.donation) > 0) return true
          if (parseFloat(sub.author.price) > 0) return true
          return false
        })

      this.newspaperSubscriptions.filter(sub => {
          if (sub.state !== 'active') return false
          if (sub.donation !== null &&  parseFloat(sub.donation) > 0) return true
          if (parseFloat(sub.newspaper.price) > 0) return true
          return false
        })
        .forEach(sub => { transactions.push(sub) })

      transactions.sort(sortBy('to'))

      return transactions
    }
  },

  methods: {
    fmtTime(datetime) {
      const format = this.$i18n.locale === 'cs' ? 'D.M.YYYY' : 'M/D/YYYY'
      return moment(datetime).format(format)
    }
  },

  async fetch({ store }) {
    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }
  }
}
</script>

<style lang="sass">
.transactions--upcoming
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
    padding: $baseline/4

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
