<template>
  <explore-view>
    <header>
      <h1>Best on Kairly</h1>
    </header>

    <section>
      <h2>Top Editions</h2>
      
      <div>
        <EditionWidget
          v-for="edition in editions"
          :key="edition.id"
          :edition="edition"
        />
      </div>
      
    </section>

    <section>
      <h2>Recommended Authors</h2>

      <AuthorWidget
        v-for="author in authors"
        :key="author.slug"
        :author="author"
      />
    </section>
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
      authors: []
    }
  },

  created() {
    this.$store.dispatch('getEditions')
    api.getAuthors().then(resp => {
      this.authors = resp.slice(10, 17)
    })
  }
}
</script>

<style lang="sass">
explore-view
  //- Header
  > header
    display: flex
    align-items: center
    justify-content: center
    height: 400px

    background: url(../assets/homepage/hero.png) center center no-repeat
    background-size: cover

    h1
      color: #fff

      font-size: 60px
      font-family: $ff-serif
      text-shadow: 0 0 10px #000


  //- Sections
  > section
    margin: $baseline auto
    width: 970px

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
