<template>
  <app-view>
    <template>
      <nuxt></nuxt>

      <portal-target name="modal" slim></portal-target>

      <InfoMessage v-if="errorMessage" type="error">{{ errorMessage }}</InfoMessage>
      <InfoMessage v-if="successMessage" type="success">{{ successMessage }}</InfoMessage>
    </template>
  </app-view>
</template>

<script>
import { mapMutations, mapState } from 'vuex'

import InfoMessage from '@/components/InfoMessage'

export default {
  name: 'app',

  middleware: ['auth'],

  components: {
    InfoMessage
  },

  computed: mapState({
    errorMessage: state => state.messages.error,
    successMessage: state => state.messages.success,
    loggedIn: state => state.auth.loggedIn,
    currentLocale: state => state.locale || 'en'
  }),

  head() {
    return {
      htmlAttrs: {
        lang: this.currentLocale,
      }
    }
  },

  watch: {
    '$route' (to, from) {
      this.clearMessages()
    }
  },

  methods: mapMutations({
    clearMessages: 'messages/clear',
  })
}
</script>

<style lang="sass">
//- Libraries
@import '../node_modules/node-reset-scss/scss/_reset'
@import '../node_modules/@fortawesome/fontawesome-free/scss/fontawesome'
@import '../node_modules/bootstrap/scss/_tooltip'
@import '../node_modules/bootstrap/scss/_popover'

//- Scaffolding
@import 'styles/scaffolding/layout'
@import 'styles/scaffolding/typography'
@import 'styles/components/mixins'

//- Components
@import 'styles/components/loading-spinner'
@import 'styles/components/tooltip'
</style>
