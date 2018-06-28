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

  metaInfo: {
    title: 'My Subscription - Authors'
  },

  components: {
    AuthorWidget
  },

  data() {
    return {
      authors: []
    }
  },

  created() {
    api.getUserAuthors().then(resp => {
      this.authors = resp
    })
  }
}
</script>

<style lang="sass">
my-editions-view author-widget-view
  width: 576px

</style>
