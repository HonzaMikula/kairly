<template>
  <AppLayout :name="$t('Credits')">
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
          <p>
            <MoneyFormat :value="user.credits" currency="Kč" />
          </p>
        </div>

        <div>
          <h3>{{ $t('Monthly spending') }}</h3>
          <p>
            <MoneyFormat :value="monthSpending" currency="Kč" />
          </p>
        </div>
      </section>

      <nav class="transactions--nav">
        <nuxt-link to="/user/transactions/upcoming">{{ $t('Upcoming payments') }}</nuxt-link>
        <nuxt-link to="/user/transactions/history">{{ $t('Past payments') }}</nuxt-link>
      </nav>

      <main>
        <nuxt-child />
      </main>
    </div>
  </AppLayout>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import MoneyFormat from '@/components/widgets/MoneyFormat'

export default {
  name: 'Transactions',

  components: {
    AppLayout,
    MoneyFormat,
  },

  computed: {
    ...mapState({
      user: state => state.auth.user,
    }),

    ...mapGetters(['monthSpending'])
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- TRANSACTIONS -//
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

//- Navigation
.transactions--nav
  display: flex
  margin-bottom: $baseline / 2

  a
    margin-right: $baseline

    color: $c-base

    font-size: $fs-2
    font-weight: 600

    &.nuxt-link-active
      border-bottom: 2px solid #000
      color: #000

</style>
