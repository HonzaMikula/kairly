<template>
  <app-view>
    <loading-spinner v-if="loadingUser"></loading-spinner>

    <template v-else>
      <router-view v-if="(user || $route.meta.public) && !loadingUser"></router-view>
      <Homepage v-else></Homepage>

      <portal-target name="modal" slim></portal-target>

      <info-message v-if="errorMessage" type="error">{{ errorMessage }}</info-message>
      <info-message v-if="successMessage" type="success">{{ successMessage }}</info-message>
    </template>
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
      errorMessage: state => state.messages.error,
      successMessage: state => state.messages.success
    }),
    ...mapGetters(['user', 'loadingUser'])
  },

  watch: {
    '$route' (to, from) {
      this.show404(false)
      this.showError(null)
      this.showSuccess(null)
    }
  },

  methods: mapMutations(['showError', 'showSuccess', 'show404']),

  created: function () {
    this.$store.dispatch('getProfile')
  }
}
</script>

<style lang="sass">
//- Libraries
@import '../node_modules/node-reset-scss/scss/_reset'
@import '../node_modules/font-awesome/scss/font-awesome'
@import '../node_modules/bootstrap/scss/_tooltip'

//- Scaffolding
@import 'styles/scaffolding/layout'
@import 'styles/scaffolding/typography'
@import 'styles/components/mixins'

//- Components
@import 'styles/components/loading-spinner'
@import 'styles/components/tooltip'
</style>
