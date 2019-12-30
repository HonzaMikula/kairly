<template>
  <AppLayout :name="$t('Search')">
    <main class="search-view">

      <header class="search--search-box">
        <input type="search" v-model="query" />
        <button @click="search()">Search</button>
      </header>

      <div
        class="search-item"
        v-for="result in results"
        :key="result.cacheId">
        <h2 v-html="result.htmlTitle.replace('– Kairly', '')"></h2>
        <p v-html="result.htmlSnippet"></p>
      </div>
    </main>
  </AppLayout>
</template>

<script>
import AppLayout from "@/components/layout/AppLayout"
import ErrorHandler from '@/mixins/ErrorHandler'

const GOOGLE_SEARCH_API = 'AIzaSyBbkq4m8pQym-r2hFYmTwStzXCNWzmom1Y'
const SEARCH_ID = '006213174493429117077:jze2yfipbxo'

export default {
  name: 'Search',

  components: {
    AppLayout
  },

  mixins: [ErrorHandler],

  data() {
    return {
      query: null,
      results: null
    }
  },

  methods: {
    async search() {
      try {
        const params = {
          key: this.GOOGLE_SEARCH_API,
          cx: this.SEARCH_ID,
          q: this.query
        }

        delete this.$axios.defaults.headers.common["Authorization"];
        const { items } = await this.$axios.$get(`https://www.googleapis.com/customsearch/v1`, { params })
        console.log(items)
        this.results = items
      } catch (err) {
        this.handleError(err)
      }
    }
  }
}
</script>

<style lang="sass">

  .search-view
    margin: $baseline auto
    max-width: 600px

    @media (max-width: $mobile)
      padding: 0 $baseline / 2

  .search--search-box
    display: flex
    max-width: 600px
    margin: 0 auto $baseline auto

    box-shadow: 4px 4px 8px #eee, -4px -4px 8px #fff

    input
      border: 1px solid #ccc
      border-radius: 5px 0 0 5px
      border-right: 0
      height: $baseline * 1.5
      flex: 1
      padding: 0 $baseline/2

      font-size: $fs-1
      font-family: $ff-sans

    button
      border-radius: 0 5px 5px 0
      height: $baseline * 1.5
      padding: 0 $baseline

      background: $c-base
      border: 0
      color: #fff

      font-family: $ff-sans
      font-size: $fs-1

  .search-item 
    margin-bottom: $baseline

    h2
      font-size: $fs-1
      font-weight: 600

    b
      font-weight: 600
</style>
