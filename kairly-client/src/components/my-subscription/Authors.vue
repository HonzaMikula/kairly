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

  computed: {
    ...mapState({
      authorIds: state => Object.keys(state.subscriptions.authors)
    }),

    // authors() {
    //    ....
    // }
  },

  created() {
    // TODO make single endpoint to fetch authors (and fetch them without editions)
    // TODO cache authors in state same as edtions are currently cached
    Promise.all(
      this.authorIds.map(id => api.getAuthorDetail(id).then(resp => resp.author))
    ).then(authors => this.authors = authors )
  }
}
</script>

<style lang="sass">
my-editions-view author-widget-view
  width: 576px

</style>
