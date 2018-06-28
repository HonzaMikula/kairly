<template>
  <app-view>
    <loading-spinner v-if="loadingUser"></loading-spinner>

    <router-view v-if="user || $route.meta.public"></router-view>
    <Homepage v-else></Homepage>

    <portal-target name="modal" slim></portal-target>
  </app-view>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import Homepage from '@/components/Homepage'

export default {
  name: 'app',

  components: {
    Homepage
  },

  metaInfo: {
      title: 'Kairly - exceptional journalism & great reading experience',
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
