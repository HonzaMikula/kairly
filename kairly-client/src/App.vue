<template>
  <app-view>
    <AppHeaderComponent />

    <span v-if="loadingUser">Loading...</span>
    <app-main v-else>
      <router-view v-if="user"></router-view>
      <Homepage v-else></Homepage>
    </app-main>
  </app-view>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import AppHeaderComponent from '@/components/AppHeaderComponent'
import Homepage from '@/components/Homepage'

export default {
  name: 'app',
  components: {
    AppHeaderComponent,
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
