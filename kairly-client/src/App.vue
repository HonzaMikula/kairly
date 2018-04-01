<template>
  <app-view>
    <Header v-if="user" />

    <loading-spinner v-if="loadingUser"></loading-spinner>
    <app-main v-else>
      <router-view v-if="user"></router-view>
      <Homepage v-else></Homepage>
    </app-main>
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
      user: state => state.user
    }),
    ...mapGetters(['loadingUser'])
  },
  created: function () {
    this.$store.dispatch('getProfile')
  }
}
</script>

<style lang="sass">
  @import 'styles/style'
</style>
