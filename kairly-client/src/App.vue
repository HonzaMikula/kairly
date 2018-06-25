<template>
  <app-view>
    <Header v-if="user" />

    <loading-spinner v-if="loadingUser"></loading-spinner>

    <app-main v-else>
      <router-view v-if="user || $route.meta.public"></router-view>
      <Homepage v-else></Homepage>
    </app-main>

    <portal-target name="modal"></portal-target>
  </app-view>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import Header from '@/components/layout/Header'
import Homepage from '@/components/Homepage'

export default {
  name: 'app',
  components: {
    Header,
    Homepage
  },

  computed: {
    ...mapState({
      showTutorial: state => state.showTutorial
    }),
    ...mapGetters(['user', 'loadingUser'])
  },

  created: function () {
    this.$store.dispatch('getProfile')
  }
}
</script>

<style lang="sass">
//- Libraries
@import '../node_modules/node-reset-scss/scss/_reset'
@import '../node_modules/font-awesome/scss/font-awesome'

//- Scaffolding
@import 'styles/scaffolding/layout'
@import 'styles/scaffolding/typography'

//- Components
@import 'styles/components/loading-spinner'
@import 'styles/components/tooltip'
</style>
