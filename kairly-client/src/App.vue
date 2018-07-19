<template>
  <app-view>
    <loading-spinner v-if="loadingUser"></loading-spinner>

    <router-view v-if="(user || $route.meta.public) && !loadingUser"></router-view>
    <Homepage v-else></Homepage>

    <portal-target name="modal" slim></portal-target>

    <portal-target name="infoMessage" slim></portal-target>

    <info-message v-if="errorMessage" type="error">{{ errorMessage }}</info-message>
  </app-view>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex'

import Homepage from '@/components/Homepage'
import InfoMessage from '@/components/InfoMessage'

export default {
  name: 'app',

  components: {
    Homepage,
    InfoMessage
  },

  metaInfo: {
      title: 'Kairly - exceptional journalism & great reading experience',
  },

  computed: {
    ...mapState({
      showTutorial: state => state.showTutorial,
      errorMessage: state => state.error
    }),
    ...mapGetters(['user', 'loadingUser'])
  },

  watch: {
    '$route' (to, from) {
      this.showError(null)
    }
  },

  methods: mapMutations(['showError']),

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
