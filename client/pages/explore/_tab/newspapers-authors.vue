<template>
  <main class="explore">
    <div class="explore--top-newspapers">
      <div>
        <NewspaperWidget
          v-for="newspaper in newspapers"
          :key="newspaper.fullName"
          :newspaper="newspaper"
        />
      </div>

    </div>

    <section :class="`explore-${index}`" v-for="(category, index) in categories" :key="index">
      <h2>{{ category.name }}</h2>
        <AuthorWidget
          v-for="author in category.authors.slice(0, LIMIT)"
          :key="author.id"
          :author="author"
        />

        <button
          v-if="category.authors.length > LIMIT"
          @click="openCategoryModal(category)"
        >
          {{ $t('Show more') }}
        </button>
    </section>

    <portal to="explore-header">{{ tab.name }}</portal>

    <ExploreModal
      :active.sync="isModalOpen"
      :category="modalCategory"
      :limit="LIMIT"
    />

  </main>
</template>

<script>
import TABS from '@/exploreTabs'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'
import ExploreModal from '@/components/modals/ExploreModal'

export default {
  name: 'ExploreTabNewspapersAuthors',

  //auth: false,

  components: {
    NewspaperWidget,
    AuthorWidget,
    ExploreModal
  },

  head() {
    const title = this.tab[this.$i18n.locale || 'en']
    return {
      title:  `${title} – Explore – Kairly`
    }
  },

  data() {
    return {
      LIMIT: 7,
      modalCategory: null,
      isModalOpen: false
    }
  },

  methods: {
    openCategoryModal(category) {
      this.modalCategory = category
      this.isModalOpen = true
    }
  },

  async asyncData({ app, store, params }) {
    const tab = TABS.find(t => t.slug === params.tab)

    const { newspapers: newspapersIds, categories } = await app.$axios.$get(`/explore/${tab.slug}`)
    const newspapers = await store.dispatch('getNewspapers', newspapersIds)

    return {
      tab,
      newspapers,
      categories
    }
  }
}
</script>

<style lang="sass">
main.explore
  display: grid
  max-width: 900px
  margin: $baseline/2 auto
  grid-column-gap: $baseline
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto auto
  grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-0 explore-1" "explore-2 explore-3"

  @media (max-width: $mobile)
    padding: 0 $baseline/4
    grid-template-columns: 100%
    grid-template-areas: "explore-top-newspapers" "explore-0" "explore-1" "explore-2" "explore-3"

  section
    > h2
      font-size: $fs-2
      font-weight: 600
      line-height: $baseline * 2

    &.explore-0
      grid-area: explore-0

    &.explore-1
      grid-area: explore-1

    &.explore-2
      grid-area: explore-2

    &.explore-3
      grid-area: explore-3

    &.explore-recent
      grid-area: explore-recent

  .explore--top-newspapers
    grid-area: explore-top-newspapers

    > h2
      font-size: $fs-2
      font-weight: 600
      line-height: $baseline * 2

    //-- wrapper
    > div
      display: grid
      grid-row-gap: $baseline
      grid-template-columns: 1fr 1fr 1fr
      grid-column-gap: $baseline / 2

      @media (max-width: $mobile)
        grid-column-gap: $baseline / 4
        overflow-x: auto
        -webkit-overflow-scrolling: touch

        .newspaper-widget-view,
        .issue-widget-view
          min-width: 200px

main.explore
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
