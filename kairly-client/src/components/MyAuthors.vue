<template>
  <div>

  </div>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import MyAuthorsItem from '@/components/MyAuthorsItem'

export default {
  name: 'MyEditions',

  components: {
    MyAuthorsItem
  },

  computed: {
    // ...mapGetters({
    //   editions: 'allEditions'
    // })
  },

  created() {
    //this.$store.dispatch('getEditions')
  }
}
</script>

<style lang="sass">
</style>
