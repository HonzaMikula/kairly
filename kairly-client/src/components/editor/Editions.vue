<template>
  <editor-editions-view>
    <editor-editions--header>
      <h1>My Editions</h1>

      <div class="create-edition" v-if="canCreateEdition">
        <a href="" v-on:click.prevent="isCreateEditionOpen=true">Start new edition</a>
      </div>
    </editor-editions--header>

    <nav v-if="editions.length">
      <editor-editions--nav-item v-for="edition in editions" :key="edition.id">
        <picture>
          <img :src="edition.picture" :alt="edition.title"/>
        </picture>

        <h2>{{edition.title}} <span>#{{ edition.issues + 1 }}</span></h2>
        <p>In <strong>4 hours</strong> with <strong>3 posts</strong>.</p>
        <span class="backlog" v-tooltip.top="'Posts in consideration'">12</span> 
      </editor-editions--nav-item>    

    </nav>

    <editor-editions--board>
      In the top editor will be switching between editions <br /><br />
      Here they will be selecting, which posts will go to upcoming issue.
    </editor-editions--board>

    <portal to="modal" v-if="isCreateEditionOpen">
      <create-edition :onClose="closeModal"></create-edition>
    </portal>
  </editor-editions-view>
</template>


<script>
import { mapState } from 'vuex'

import * as api from '@/api'

import EditionWidget from '@/components/widgets/EditionWidget'
import CreateEdition from '@/components/editor/CreateEdition'

export default {
  name: 'AuthorDetail',
  components: {
    EditionWidget,
    CreateEdition
  },

  data() {
    return {
      loadingProfile: true,
      author: null,
      topic: null,
      editionIds: [],
      cursor: null,
      isCreateEditionOpen: false
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
    closeModal() {
      this.isCreateEditionOpen = false
      this.$forceUpdate()
    },

    loadData() {
      const { authorId } = this.$route.params

      this.loadingProfile = true
      this.loadingPosts = true
      this.author = null
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
  margin: 0 $baseline

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

  //- Switcher between Editions
  > nav
    display: flex
    
    overflow: hidden


editor-editions--nav-item
  position: relative
  margin-right: $baseline / 2

  background: #fff
  opacity: 0.7

  &:nth-of-type(2)
    opacity: 1

    border-bottom: 5px solid $c-base

  picture 
    
    img
      height: $baseline * 4
      width: 250px
      object-fit: cover

  h2
    font-weight: 600 
    font-family: $ff-sans
    font-size: $fs--1

    span
      float: right

  p 
    font-size: $fs--2  

  .release
    position: absolute
    left: $baseline / 4
    top: $baseline / 4

    border-radius: 100%
    display: inline-block
    height: $baseline
    width: $baseline

    background: $c-base
    color: #fff

    font-weight: 600
    font-size: $fs--2
    text-align: center

  .backlog
    position: absolute
    right: $baseline / 4
    top: $baseline / 4

    border-radius: 100%
    display: inline-block
    height: $baseline
    width: $baseline

    background: #fff
    color: #000

    font-size: $fs--2
    text-align: center
  
editor-editions--board
  display: block
  height: 400px
  padding: $baseline
  margin-top: $baseline

  background: #eee

  text-align: center


</style>
