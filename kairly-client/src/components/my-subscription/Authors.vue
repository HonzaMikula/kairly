<template>
  <div>
    <my-authors--empty
      v-if="authors.length === 0">
      <h1>No authors</h1>
      <p>You haven't subscribe to any author yet. On Explore page you can find authors you might like.</p>
      <router-link to="/explore">Explore authors</router-link>
    </my-authors--empty>

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
    // TODO make single endpoint to fetch authors (and fetch them without newspapers)
    // TODO cache authors in state same as edtions are currently cached
    Promise.all(
      this.authorIds.map(id => api.getAuthorDetail(id).then(resp => resp.author))
    ).then(authors => this.authors = authors )
  }
}
</script>

<style lang="sass">
my-newspapers-view author-widget-view
  width: 576px

my-authors--empty
  display: block
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  p
    margin-bottom: $baseline

  a
    +subscribed-button

    display: inline-block

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
