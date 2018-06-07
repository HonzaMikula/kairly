<template>
  <explore-view class="politics">
    <header>
      <nav>
        <ul>
          <li><a href="/explore">Best of Kairly</a></li>
          <li><a href="/explore/politics" class="is-active">Politics</a></li>
          <li><a href="">Sport</a></li>
          <li><a href="">Technology</a></li>
          <li><a href="">Lifestyle</a></li>
        </ul>
      </nav>
      <h1>Politics</h1>
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

      <section class="news">
        <h2>News</h2>

        <AuthorWidget
          v-for="author in newsAuthors"
          :key="author.slug"
          :author="author"
        />
      </section>

      <section class="politics">
        <h2>Politics</h2>

        <AuthorWidget
          v-for="author in politicsAuthors"
          :key="author.slug"
          :author="author"
        />
      </section>

      <section class="journalist">
        <h2>Journalists & Commentators</h2>

        <AuthorWidget
          v-for="author in journalistAuthors"
          :key="author.slug"
          :author="author"
        />
      </section>

      <section class="thinkThanks">
        <h2>Think-thanks</h2>

        <AuthorWidget
          v-for="author in thinkThanksAuthors"
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
      newsAuthors: [],
      politicsAuthors: [],
      journalistAuthors: [],
      thinkThanksAuthors: []
    }
  },

  created() {
    this.$store.dispatch('getEditions')
    api.getAuthors().then(resp => {
      this.newsAuthors = resp.slice(1, 4)
      this.politicsAuthors = resp.slice(7, 10)
      this.journalistAuthors = resp.slice(13, 16)
      this.thinkThanksAuthors = resp.slice(17, 20)
    })
  }
}
</script>

<style lang="sass">
explore-view.politics
  
  //- Header
  > header
    display: grid
    grid-template-columns: 100%
    grid-template-rows: auto $baseline*2
    grid-template-areas: "heading" "nav"

    height: 400px

    background: url(http://kairly.com/media/editions/uspolitics.jpg) center center no-repeat
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
    grid-template-areas: "explore-top-editions explore-top-editions" "explore-news explore-politics" "explore-journalist explore-think-thanks"

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

section
  > h2
    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 2

  &.news
    grid-area: explore-news

  &.politics
    grid-area: explore-politics

  &.journalist
    grid-area: explore-journalist

  &.thinkThanks
    grid-area: explore-think-thanks      



</style>
