<template>
  <app-layout :name="$t('Add Credit')">
    <div>
      Kairly is currently in beta. You will receive free credit automatically every month.
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
</style>
