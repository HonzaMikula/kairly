<template>
  <main>
    <explore--top-newspapers>
      <h2>{{this.tab.newspapersTitle}}</h2>

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
          v-for="author in category.authors.slice(0, 7)"
          :key="author.id"
          :author="author"
        />

        <button v-if="category.authors.length > 7" @click="openCategoryModal(category)">
          Show more
        </button>
    </section>

    <portal to="modal" v-if="showCaregoryInModal">
      <explore-modal :closeModal="closeCategoryModal" :category="showCaregoryInModal" />
    </portal>
  </main>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'
import ExploreModal from '@/components/explore/ExploreModal'

export default {
  name: 'ExploreContent',

  components: {
    NewspaperWidget,
    AuthorWidget,
    ExploreModal
  },

  props: {
    tab: Object
  },

  data() {
    return {
      categories: [],
      showCaregoryInModal: null
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
    },

    openCategoryModal(category) {
      this.showCaregoryInModal = category
    },

    closeCategoryModal() {
      this.showCaregoryInModal = null
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
/* COPY PASTE FROM IssueWrapper.vue */

section button
  display: table
  border-radius: $baseline
  height: $baseline * 1.25
  padding: 0 $baseline
  margin: 0 auto

  background: $c-base
  border: 0
  color: #fff

  font-family: $ff-sans
  font-size: $fs--1
  line-height: $baseline * 1.25
  cursor: pointer

  &:hover,
  &:focus
    background: darken($c-base, 10%)


</style>
