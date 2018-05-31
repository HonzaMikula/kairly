<template>
  <div>
    <MyAuthorsItem
      v-for="author in authors"
      :key="author.slug"
      :author="author"
    />
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
