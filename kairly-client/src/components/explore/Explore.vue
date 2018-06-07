<template>
  <explore-view class="bestOf">
    <header>
      <nav>
        <ul>
          <li><a href="/explore" class="is-active">Best of Kairly</a></li>
          <li><a href="/explore/politics">Politics</a></li>
          <li><a href="">Sport</a></li>
          <li><a href="">Technology</a></li>
          <li><a href="">Lifestyle</a></li>
        </ul>
      </nav>
      <h1>Best on Kairly</h1>
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

      <section class="recommended-authors">
        <h2>Recommended Authors</h2>

        <AuthorWidget
          v-for="author in recommendedAuthors"
          :key="author.slug"
          :author="author"
        />
      </section>

      <section class="most-read-authors">
        <h2>Most Read Authors</h2>

        <AuthorWidget
          v-for="author in topReadAuthors"
          :key="author.slug"
          :author="author"
        />
      </section>
    </main>
  </explore-view>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

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
      return (this.allEditions || []).slice(0, 3)
    }
  },

  data() {
    return {
      recommendedAuthors: [],
      topReadAuthors: []
    }
  },

  created() {
    this.$store.dispatch('getEditions')
    api.getAuthors().then(resp => {
      this.recommendedAuthors = resp.slice(7, 12)
      this.topReadAuthors = resp.slice(17, 22)
    })
  }
}
</script>

<style lang="sass">
explore-view.bestOf
  
  //- Header
  > header
    display: grid
    grid-template-columns: 100%
    grid-template-rows: auto $baseline*2
    grid-template-areas: "heading" "nav"

    height: 400px

    background: url(../../assets/homepage/hero.png) center center no-repeat
    background-size: cover

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
    grid-template-areas: "explore-top-editions explore-top-editions" "explore-recommended-authors explore-most-read-authors"

  section
    > h2
      font-size: $fs-2
      font-weight: 600
      line-height: $baseline * 2

    &.recommended-authors
      grid-area: explore-recommended-authors

    &.most-read-authors  
      grid-area: explore-most-read-authors

explore--top-editions
  grid-area: explore-top-editions

  > h2
    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 2

  //-- wrapper
  > div  
    display: flex
    flex-wrap: wrap
    margin: 0 (-$baseline/4)

</style>
