<template>
  <app-view>
    <AppHeaderComponent />

    <app-main v-if="user">
      <router-view></router-view>
    </app-main>
  </app-view>
</template>

<script>
import { mapState } from 'vuex'

import AppHeaderComponent from '@/components/AppHeaderComponent'

export default {
  name: 'app',
  components: {
    AppHeaderComponent
  },
  computed: mapState({
    user: state => state.user
  }),
  created: function () {
    this.$store.dispatch('getProfile')
  }
}
</script>

<style lang="sass">
  @import 'styles/style'
</style>
