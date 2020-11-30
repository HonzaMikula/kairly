<template>
  <AppLayout :name="$t('Search')">
    <main class="search-view">
      <header class="search--search-box">
        <input v-model="query" type="search" autofocus @keyup.enter="search()">
        <button @click="search()">{{ $t('Search') }}</button>
      </header>
      <aside
        v-if="totalResults > 0"
        class="search--total-results"
      >
        {{ totalResults }} results
      </aside>

      <template v-if="totalResults > 0">
        <div
          v-for="result in results"
          :key="result.cacheId"
          class="search-item"
        >
          <h2>
            <nuxt-link
              :to="result.link.replace('https://kairly.com/', '')"
              v-html="result.htmlTitle.replace('– Kairly', '')"
            />
          </h2>

          <img
            v-if="result.pagemap.metatags[0]['og:image']"
            :src="result.pagemap.metatags[0]['og:image']"
            :alt="result.pagemap.metatags.og_image_alt"
          >

          <div class="search-item--label">
            <template v-if="result.pagemap.newspaper">
              <span class="label">{{ $t('Newsletter') }}</span>
              <span class="author">{{ $t('by') }} {{ result.pagemap.metatags[0].author }}</span>
              <time>{{ result.pagemap.newspaper[0].datepublished | moment('calendar') }}</time>
            </template>

            <templave v-else-if="result.pagemap.metatags[0]['og:type'] == 'profile'">
              <span class="label">{{ $t('Author') }}</span>
            </templave>

            <template v-else-if="result.pagemap.newsarticle">
              <span class="label">{{ $t('Article') }}</span>
              <span class="author">{{ $t('by') }}  {{ result.pagemap.person[0].name }}</span>
              <time>{{ result.pagemap.newsarticle[0].datepublished | moment('calendar') }}</time>
            </template>
          </div>
          <p v-html="result.htmlSnippet" />
        </div>
      </template>

      <template v-else-if="totalResults !== null">
        <div class="search-no-results">
          {{ $t('No results were found for') }} "{{ query }}".
        </div>
      </template>

      <footer
        v-if="numberOfPages > 0"
        class="search--pagination"
      >
        <ul>
          <li
            v-for="page in numberOfPages"
            :key="page"
            :class="{'is-active': page == currentPage}"
            @click="pagination(page)"
          >
            {{ page }}
          </li>
        </ul>
      </footer>
    </main>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'Search',

  components: {
    AppLayout
  },

  mixins: [ErrorHandler],

  data () {
    return {
      query: null,
      results: null,
      totalResults: null,
      startResult: null,
      numberOfPages: 0,
      currentPage: 1
    }
  },

  head () {
    return {
      title: this.$t('Search – Kairly')
    }
  },

  methods: {
    async search () {
      if (this.query) {
        try {
          const adapter = this.$axios.create({
            baseURL: 'https://www.googleapis.com/',
          })
          delete adapter.defaults.headers.common.Authorization
          const searchResults = await adapter.$get('customsearch/v1', {
            params: {
              key: 'AIzaSyBbkq4m8pQym-r2hFYmTwStzXCNWzmom1Y',
              cx: '006213174493429117077:jze2yfipbxo',
              q: this.query,
              start: this.startResult
            }
          })
          const { items, searchInformation } = searchResults
          this.results = items
          this.totalResults = searchInformation.totalResults
          this.numberOfPages = Math.ceil(this.totalResults / 10)

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
    },

    pagination (page) {
      this.startResult = page * 10 + 1
      this.currentPage = page

      this.search()
      window.scrollTo(0, 0)
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
    margin: 0 auto

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

  //- Total Results
  .search--total-results
    margin-bottom: $baseline

    font-size: $fs--2

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

  .search--pagination
    margin: $baseline 0

    ul
      display: flex
      justify-content: center
      flex-wrap: wrap

    li

      border-radius: 100%
      margin-right: $baseline / 4
      margin-bottom: $baseline / 2
      height: $baseline * 1.25
      width: $baseline * 1.25

      background: #eee

      cursor: pointer
      font-weight: 600
      line-height: $baseline * 1.25
      text-align: center

      &:hover,
      &:focus
        background: #ddd

      &.is-active
        background: $c-base
        color: #fff

  //- When there is no results find
  .search-no-results
    margin-top: $baseline

    text-align: center
</style>
