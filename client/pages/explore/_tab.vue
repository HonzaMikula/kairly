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
          v-for="author in category.authors.slice(0, LIMIT)"
          :key="author.id"
          :author="author"
        />

        <button v-if="category.authors.length > LIMIT" @click="openCategoryModal(category)">
          Show more
        </button>
    </section>

    <portal to="explore-header">{{ tab.name }}</portal>

    <portal to="modal" v-if="showCaregoryInModal">
      <explore-modal :closeModal="closeCategoryModal"
        :category="showCaregoryInModal" :limit="LIMIT" />
    </portal>
  </main>
</template>

<script>
import TABS from '@/exploreTabs'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'
import ExploreModal from '@/components/explore/ExploreModal'

export default {
  name: 'ExploreTab',

  //auth: false,

  components: {
    NewspaperWidget,
    AuthorWidget,
    ExploreModal
  },

  head() {
    return {
      title: this.tab ? `${this.tab.name} – Explore – Kairly` : 'Explore – Kairly',
    }
  },

  data() {
    return {
      LIMIT: 7,
      showCaregoryInModal: null
    }
  },

  methods: {
    openCategoryModal(category) {
      this.showCaregoryInModal = category
    },

    closeCategoryModal() {
      this.showCaregoryInModal = null
    }
  },

  async asyncData({ app, store, params }) {
    const tab = TABS.find(t => t.slug === params.tab)
    const [newspapers, { categories }] = await Promise.all([
      store.dispatch('getNewspapers', tab.newspapers),
      app.$axios.$get(`/explore/${tab.name}`)
    ])
    return {
      tab,
      newspapers,
      categories
    }
  }
}
</script>

<style lang="sass">
explore-view
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
    font-size: $fs-0
    line-height: $baseline * 1.25
    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)


</style>
