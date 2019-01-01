<template>
  <app-layout :name="$t('Add Credit')">
    <div class="buy-credits-view">
      <h1>Buy Credits</h1>

      <p>
        Kairly is currently in beta. You will receive free credit automatically every month.
      </p>

      <p>In future you will have to buy credit. But we will also start paying authors and editors for their good work.</p>
    </div>
  </app-layout>
</template>

<script>


import AppLayout from '@/components/layout/AppLayout'


export default {
  name: 'AddCredit',

  head() {
    return {
      title: this.$t('Add Credit – Kairly')
    }
  },

  components: {
    AppLayout,
  }
}
</script>

<style lang="sass">
//- BUY CREDITS VIEW -//
.buy-credits-view
  max-width: 900px
  margin: 0 auto
  padding: $baseline 0

  //- Heading
  > h1
    margin-bottom: $baseline

    font-weight: 600
    font-size: $fs-3

</style>
