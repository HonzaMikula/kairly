<template>
  <div>
    <EditionWidget
      v-for="edition in editions"
      :key="edition.id"
      :edition="edition"
    />
  </div>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import EditionWidget from '@/components/widgets/EditionWidget'

export default {
  name: 'MyEditions',

  components: {
    EditionWidget
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
