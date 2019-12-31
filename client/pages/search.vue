<template>
  <AppLayout :name="$t('Search')">
    <main class="search-view">

      <header class="search--search-box">
        <input type="search" @keyup.enter="search()" v-model="query" autofocus />
        <button @click="search()">Search</button>
      </header>

      <div
        class="search-item"
        v-for="result in testResults"
        :key="result.cacheId">
        <h2>
          <nuxt-link 
            :to="result.link.replace('https://kairly.com/', '')"
            v-html="result.htmlTitle.replace('– Kairly', '')">
          </nuxt-link>
        </h2>
        
        <img 
          v-if="result.pagemap.metatags[0]['og:image']"
          :src="result.pagemap.metatags[0]['og:image']" 
          :alt="result.pagemap.metatags.og_image_alt"
        />

        <div class="search-item--label">
          <template v-if="result.pagemap.newspaper">
            <span class="label">Newspaper</span>
            <span class="author">by {{ result.pagemap.metatags[0].author }}</span>
            <time>{{ result.pagemap.newspaper[0].datepublished | moment('calendar') }}</time>
          </template>

          <templave v-else-if="result.pagemap.metatags[0]['og:type'] == 'profile'">
            <span class="label">Author</span>
          </templave>

          <template v-else-if="result.pagemap.newsarticle">
            <span class="label">Article</span>
            <span class="author">by {{ result.pagemap.metatags[0].author }}</span>
            <time>{{ result.pagemap.newsarticle[0].datepublished | moment('calendar') }}</time>
          </template>
        </div>
        <p v-html="result.htmlSnippet"></p>
        
      </div>
    </main>
  </AppLayout>
</template>

<script>
import RESULTS from '@/searchResults'
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

  head() {
    return {
      title: this.$t('Search – Kairly')
    }
  },

  data() {
    return {
      query: null,
      results: null,
      testResults: RESULTS
    }
  },

  methods: {
    async search() {

      if (this.query) {
        console.log(this.testResults)
        try {
          const params = {
            key: this.GOOGLE_SEARCH_API,
            cx: this.SEARCH_ID,
            q: this.query
          }

          // remove default authorization header
          // To Do: it removes from all Axios request, which makes the app unusable
          delete this.$axios.defaults.headers.common["Authorization"] 
          const { items } = await this.$axios.$get(`https://www.googleapis.com/customsearch/v1`, { params })
          console.log(items)
          this.results = items

          this.$ga.event({
            eventCategory: 'Search',
            eventAction: 'Search page',
            eventLabel: this.query
          })
        } catch (err) {
          this.handleError(err)

          this.$ga.event({
            eventCategory: 'Search',
            eventAction: 'Error',
            eventLabel: err
          })
        }
      }
    }
  }
}
</script>

<style lang="sass">

  .search-view
    margin: $baseline auto 0 auto
    max-width: 600px
    padding-bottom: $baseline

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
      
      cursor: pointer

      &:hover,
      &:focus
        background: darken($c-base, 10%)

  //- Search Results
  .search-item 
    display: grid
    grid-template-columns: $baseline*5 1fr
    grid-column-gap: $baseline/2
    margin-bottom: $baseline

    @media (max-width: $mobile)
      grid-template-columns: auto

    h2
      grid-column: 2
      font-size: $fs-1
      font-weight: 600
      line-height: 1.42

      @media (max-width: $mobile)
        grid-area: auto

      a
        color: darken($c-base, 20%)

        &:visited
          color: darken($c-base, 30%)

    b
      font-weight: 600

    img
      grid-column: 1
      grid-row: 1 / span 5
      height: $baseline * 3
      width: $baseline * 5

      object-fit: cover

      @media (max-width: $mobile)
        grid-area: auto
        width: 100%
        height: $baseline * 5
        margin: $baseline/4 0

    p
      grid-column: 2

      line-height: 1.42

      @media (max-width: $mobile)
        grid-area: auto

    p br
      display: none
  
  //- Label - newspaper, issue, author, article
  .search-item--label
    grid-column: 2

    @media (max-width: $mobile)
      grid-area: auto
    
    color: #555

    font-size: $fs--2

    .label
      display: inline-block
      border-radius: 3px
      padding: 0 $baseline/4

      background: #ddd

      font-size: $fs--2
      line-height: 1.42

    .author
      &::before,
      &::after
        content: ' • '

</style>
