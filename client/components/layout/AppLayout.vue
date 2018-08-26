<template>
  <app-main>
    <AppHeader v-if="loggedIn" />
    <slot></slot>
  </app-main>
</template>

<script>
import { mapState } from 'vuex'

import AppHeader from '@/components/layout/Header'

export default {
  name: 'AppLayout',

  components: {
    AppHeader
  },

  computed: mapState({
    loggedIn: state => state.auth.loggedIn
  })
}
</script>

<style lang="sass">
</style>
