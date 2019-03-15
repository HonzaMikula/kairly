<template>
  <app-main>
    <AppHeader
      v-if="loggedIn"
      :pageTitle="name"
    />
    <AppHeaderPublic v-else />

    <slot></slot>
  </app-main>
</template>

<script>
import { mapState } from 'vuex'

import AppHeader from '@/components/layout/AppHeader'
import AppHeaderPublic from '@/components/layout/AppHeaderPublic'

export default {
  name: 'AppLayout',

  components: {
    AppHeader,
    AppHeaderPublic
  },

  props: {
    name: String
  },

  computed: mapState({
    loggedIn: state => state.auth.loggedIn
  })
}
</script>

<style lang="sass">
</style>
