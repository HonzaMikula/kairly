<template>
  <app-main>
    <AppHeader v-if="loggedIn" />
    <AppHeaderPublic v-else />
    <slot></slot>
  </app-main>
</template>

<script>
import { mapState } from 'vuex'

import AppHeader from '@/components/layout/Header'
import AppHeaderPublic from '@/components/layout/HeaderPublic'

export default {
  name: 'AppLayout',

  components: {
    AppHeader,
    AppHeaderPublic
  },

  computed: mapState({
    loggedIn: state => state.auth.loggedIn
  })
}
</script>

<style lang="sass">
</style>
