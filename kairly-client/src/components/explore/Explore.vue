<template>
  <explore-view :class="tab.slug">
    <header>
      <nav>
        <ul>
          <li v-for="tab in tabs" :key="tab.slug"><router-link :to="tab.slug ? '/explore/' + tab.slug : '/explore'" exact>{{ tab.name }}</router-link></li>
        </ul>
      </nav>
      <h1>{{ tab.name }}</h1>
    </header>

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
  </explore-view>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'
import TABS from './exploreTabs'

import EditionWidget from '@/components/widgets/EditionWidget'
import AuthorWidget from '@/components/widgets/AuthorWidget'

export default {
  name: 'Explore',

  components: {
    EditionWidget,
    AuthorWidget
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

  data() {
    return {
      tabs: TABS,
      tab: null,
      authors: {}
    }
  },

  methods: {
    loadData() {
      const slug = this.$route.params.tab
      this.tab = TABS.find(t => t.slug === slug)

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
explore-view

  //- Header
  > header
    display: grid
    grid-template-columns: 100%
    grid-template-rows: auto $baseline*2
    grid-template-areas: "heading" "nav"

    height: 400px

    background: url(../../assets/homepage/hero.png) center center no-repeat
    background-size: cover

    @at-root .politics > header
      background-image: url(http://kairly.com/media/editions/uspolitics.jpg)

    @at-root .sport > header
      background-image: url(http://kairly.com/media/editions/olymp.jpg)

    @at-root .technology > header
      background-image: url(http://kairly.com/media/editions/bitcoin.jpg)    

    @at-root .lifestyle > header
      background-image: url(http://www.celiaxmoni.cz/wp-content/uploads/2018/05/222C8379-5FE4-42C4-91B9-4C441AC7AC6F.jpeg)   

    nav
      grid-area: nav

      backdrop-filter: blur(5px)
      background: rgba(0, 0, 0, 0.05)

      ul
        display: table
        margin: 0 auto

      li
        display: inline-block

      a
        display: block
        padding: 0 $baseline/2

        color: #fff

        line-height: $baseline * 2
        text-decoration: none

        &:hover,
        &:focus,
        &.is-active
          background: rgba(0, 0, 0, 0.3)



    h1
      grid-area: heading
      align-self: center
      justify-self: center

      color: #fff

      font-size: 60px
      font-family: $ff-serif
      text-shadow: 0 0 10px #000


  //- Sections
  main
    display: grid
    max-width: 970px
    margin: $baseline auto
    grid-column-gap: $baseline
    grid-row-gap: $baseline
    grid-template-columns: 50% 50%
    grid-template-rows: auto auto
    grid-template-areas: "explore-top-editions explore-top-editions" "explore-0 explore-1" "explore-2 explore-3"

explore--top-editions
  grid-area: explore-top-editions

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



</style>
