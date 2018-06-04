<template>
  <div>
    <h1>Explore</h1>
  </div>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'ExploreSubscription',

  components: {
  },

  computed: {
    ...mapGetters({
      editions: 'allEditions'
    })
  },

  created() {
    this.$store.dispatch('getEditions')
  }
}
</script>

<style lang="sass">
</style>
