<template>
  <app-layout :name="$t('Transactions')">
    <div>
      <nav>
        <nuxt-link to="/user/transactions/history">{{ $t('History') }}</nuxt-link>
        <nuxt-link to="/user/transactions/upcomming">{{ $t('Upcomming') }}</nuxt-link>
      </nav>

      <main>
        <nuxt-child/>
      </main>
    </div>
  </app-layout>
</template>

<script>
import { mapState, mapGetters } from 'vuex'


import AppLayout from '@/components/layout/AppLayout'


export default {
  name: 'Transactions',

  components: {
    AppLayout,
  }
}
</script>

<style lang="sass">
</style>
