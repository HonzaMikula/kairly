<template>
  <div>
    <AppHeader
      v-if="loggedIn"
      :page-title="name"
    />
    <AppHeaderPublic v-else />

    <slot />
  </div>
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
    name: { type: String, default: null }
  },

  computed: mapState({
    loggedIn: state => state.auth.loggedIn
  }),

  mounted () {
    if (this.loggedIn) {
      this.$ga.set('dimension1', 'yes')
    } else {
      this.$ga.set('dimension1', 'no')
    }
  },
}
</script>

<style lang="sass">
</style>
