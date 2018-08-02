<template>
  <main>
    <explore--top-newspapers>
      <h2>Top Newspapers</h2>

      <div>
        <NewspaperWidget
          v-for="newspaper in newspapers"
          :key="newspaper.fullName"
          :newspaper="newspaper"
        />
      </div>

    </explore--top-newspapers>

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

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'ExploreContent',

  components: {
    NewspaperWidget,
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
    newspapers() {
      return this.tab.newspapers
        .map(id => this.$store.getters.newspaper(id))
        .filter(newspaper => newspaper !== undefined)
    }
  },

  methods: {
    loadData() {
      this.$store.dispatch('getNewspapers', this.tab.newspapers)

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
