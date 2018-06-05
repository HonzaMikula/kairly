<template>
  <div>
    <AuthorWidget
      v-for="author in authors"
      :key="author.slug"
      :author="author"
    />
  </div>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'MyAuthors',

  components: {
    AuthorWidget
  },

  data() {
    return {
      authors: []
    }
  },

  created() {
    api.getAuthors().then(resp => {
      this.authors = resp
    })
  }
}
</script>

<style lang="sass">
</style>
