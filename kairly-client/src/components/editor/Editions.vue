<template>
  <editor-editions-view>
    <editor-editions--header>
      <h1>My Editions</h1>

      <div class="create-edition" v-if="canCreateEdition">
        <router-link :to="{ name: 'create-edition', params: {authorId: this.$route.params.authorId} }">Start new edition</router-link>
      </div>
    </editor-editions--header>

    <author-detail--editions v-if="editions.length">

      <div>
        <EditionWidget
          v-for="edition in editions"
          :key="edition.id"
          v-bind:edition="edition"
        />
      </div>

    </author-detail--editions>

  </editor-editions-view>
</template>


<script>
import { mapState } from 'vuex'

import * as api from '@/api'

import EditionWidget from '@/components/widgets/EditionWidget'

export default {
  name: 'AuthorDetail',
  components: {
    EditionWidget
  },

  data() {
    return {
      loadingProfile: true,
      loadingPosts: true,
      author: null,
      topic: null,
      editionIds: [],
      posts: [],
      cursor: null
    }
  },

  computed: {
    editions() {
      const ids = this.editionIds
      return ids.map(id => this.$store.getters.edition(id))
    },

    canCreateEdition() {
      return this.user.author && this.author && this.user.author.id == this.author.id
    },

    ...mapState({
      user: state => state.user
    }),
  },

  watch: {
    '$route' (to, from) {
      this.loadData()
    }
  },

  methods: {
    toggleEditions() {
      this.showAllEditions = !this.showAllEditions
    },

    handlePostsData(resp) {
      resp.posts.forEach(post => this.posts.push(post))
      this.cursor = resp.cursor
      this.loadingPosts = false
    },

    loadMore() {
      if (this.cursor) {
        const { authorId } = this.$route.params

        this.loadingPosts = true
        api.getAuthorPosts(authorId, this.cursor).then(this.handlePostsData)
      }
    },

    loadData() {
      const { authorId } = this.$route.params

      this.loadingProfile = true
      this.loadingPosts = true
      this.author = null
      this.showAllEditions = false
      this.editionIds = []
      this.posts = []
      this.cursor = null

      api.getAuthorDetail(authorId).then(resp => {
        resp.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
        this.author = resp.author
        this.editionIds = resp.editions.map(e => e.id)
        this.loadingProfile = false
        this.topics = resp.topics
      })
      api.getAuthorPosts(authorId, null).then(this.handlePostsData)
    }
  },

  created() {
    this.loadData()
  },
}
</script>

<style lang="sass">
editor-editions-view
  position: relative

  display: block
  margin: 0 auto
  max-width: 900px

//- Header
editor-editions--header
  display: block
  padding: $baseline 0

  h1
    font-family: $ff-serif
    font-size: $fs-2
    font-weight: 600

  .create-edition
    position: absolute
    right: 0
    top: $baseline

    a
      +subscribe-button

      display: inline-block
      height: $baseline * 1.5
      border-radius: $baseline * 0.75
      padding: 0 $baseline/2

      font-family: $ff-sans
      line-height: $baseline * 1.5
</style>
