<template>
  <main>
    <explore--top-editions>
      <h2>Top Editions</h2>

      <div>
        <EditionWidget
          v-for="edition in editions"
          :key="edition.id"
          :edition="edition"
        />
      </div>

    </explore--top-editions>

    <section :class="`explore-${index}`" v-for="(section, index) in tab.sections" :key="index">
      <h2>{{ section.name }}</h2>

      <div v-for="authorId in section.authors" :key="authorId">
        <AuthorWidget
          v-if="authors[authorId]"
          :key="authorId"
          :author="authors[authorId]"
        />
      </div>
    </section>
  </main>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import EditionWidget from '@/components/widgets/EditionWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'ExploreContent',

  components: {
    EditionWidget,
    AuthorWidget
  },

  props: {
    tab: Object
  },

  data() {
    return {
      authors: {}
    }
  },

  computed: {
    ...mapGetters(['allEditions']),

    editions() {
      return (this.tab.editions
        .map(id => (this.allEditions || []).find(e => e.id === id))
        .filter(edition => edition !== undefined)
      )
    }
  },

  methods: {
    loadData() {
      const authors = []
      this.tab.sections.forEach(section => authors.push(...section.authors))
      Promise.all(authors.map(authorId => {
        const params = authorId.split('/')
        return api.getAuthorDetail(...authorId.split('/')).then(res => {
          // save loaded edition to store
          res.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
          this.authors = {...this.authors, [authorId]: res.author}
          return res.author
        })
      }))
    }
  },

  watch: {
    '$route' (to, from) {
      this.loadData()
    }
  },

  created() {
    // TODO in future replace with loading only used editions
    this.$store.dispatch('getEditions')
    this.loadData()
  }
}
</script>

<style lang="sass">
</style>
