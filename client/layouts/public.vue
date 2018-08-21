<template>
  <app-view>
    <template>
      <nuxt></nuxt>

      <portal-target name="modal" slim></portal-target>

      <info-message v-if="errorMessage" type="error">{{ errorMessage }}</info-message>
      <info-message v-if="successMessage" type="success">{{ successMessage }}</info-message>
    </template>
  </app-view>
</template>

<script>
import { mapGetters, mapMutations, mapState } from 'vuex'

import InfoMessage from '@/components/InfoMessage'

export default {
  name: 'app',

  components: {
    InfoMessage
  },

  computed: {
    ...mapState({
      errorMessage: state => state.messages.error,
      successMessage: state => state.messages.success
    })
  },

  watch: {
    '$route' (to, from) {
      this.show404(false)
      this.showError(null)
      this.showSuccess(null)
    }
  },

  methods: mapMutations(['showError', 'showSuccess', 'show404']),
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
