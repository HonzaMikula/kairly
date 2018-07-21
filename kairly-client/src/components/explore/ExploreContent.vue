<template>
  <main>
    <explore--top-editions>
      <h2>Top Editions</h2>

      <div>
        <EditionWidget
          v-for="edition in editions"
          :key="edition.fullName"
          :edition="edition"
        />
      </div>

    </explore--top-editions>

    <section :class="`explore-${index}`" v-for="(category, index) in categories" :key="index">
      <h2>{{ category.name }}</h2>
        <AuthorWidget
          v-for="author in category.authors"
          :key="category.id"
          :author="author"
        />
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
      categories: []
    }
  },

  computed: {
    editions() {
      return this.tab.editions
        .map(id => this.$store.getters.edition(id))
        .filter(edition => edition !== undefined)
    }
  },

  methods: {
    loadData() {
      this.$store.dispatch('getEditions', this.tab.editions)

      // TODO nice to have cache result + cache authors in store !
      api.getExploreTab(this.tab.name).then(payload => this.categories = payload.categories)
    }
  },

  watch: {
    '$route' (to, from) {
      this.loadData()
    }
  },

  created() {
    this.loadData()
  }
}
</script>

<style lang="sass">
</style>
