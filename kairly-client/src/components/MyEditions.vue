<template>
  <div>
    <MyEditionsItem
      v-for="edition in editions"
      :key="edition.id"
      v-bind:edition="edition"
    />
  </div>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'MyEditions',

  components: {
    MyEditionsItem
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
