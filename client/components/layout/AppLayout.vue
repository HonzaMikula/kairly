<template>
  <app-main>
    <AppHeader />
    <not-found v-if="show404"></not-found>
    <slot v-else></slot>
  </app-main>
</template>

<script>
import { mapState } from 'vuex'

import AppHeader from '@/components/layout/Header'
import NotFound from '@/components/NotFound'

export default {
  name: 'AppLayout',

  components: {
    AppHeader,
    NotFound
  },

  computed: mapState({
    show404: state => state.show404,
  })
}
</script>

<style lang="sass">
</style>
