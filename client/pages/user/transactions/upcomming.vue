<template>
  <div>
    <div v-for="t in transactions">
      <div v-if="t.author" style="display: flex">
        {{ t.author.name }} *
        {{ fmtTime(t.to) }} *
        <AuthorSubscription :author="t.author" />
      </div>
      <div v-if="t.newspaper" style="display: flex">
        {{ t.newspaper.name}} *
        {{ fmtTime(t.to) }} *
        <NewspaperSubscription :newspaper="t.newspaper" />
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

import { sortBy } from '@/utils/array'

import AuthorSubscription from '@/components/widgets/AuthorSubscription'
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'

export default {
  name: 'UpcommingTransactions',

  head() {
    return {
      title: this.$t('Upcoming transactions') + ' – Kairly'
    }
  },

  components: {
    AuthorSubscription,
    NewspaperSubscription
  },

  computed: {
    transactions() {
      const { authors, newspapers } = this.$store.state.subscriptions
      const transactions = Object.values(authors)
        .filter(sub => {
          if (sub.state !== 'active') return false
          if (sub.donation !== null &&  parseFloat(sub.donation) > 0) return true
          if (parseFloat(sub.author.price) > 0) return true
          return false
        })

      Object.entries(newspapers)
        .map(([id, sub]) => {
          const newspaper = this.$store.getters.newspaper(id)
          return {newspaper, ...sub}
        })
        .filter(sub => {
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
      const format = this.$i18n.locale === 'cs' ? 'D.M.YYYY HH:mm' : 'M/D/YYYY HH:mm'
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
</style>
