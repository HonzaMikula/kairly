<template>
  <editor-editions-view>
    <editor-editions--header>
      <h1>My Editions</h1>

      <div class="create-edition">
        <a href="" @click.prevent="isCreateEditionOpen = true">Start new edition</a>
      </div>
    </editor-editions--header>

    <nav>
      <editor-editions--nav-item 
        v-for="edition in editions" 
        :key="edition.id" 
        @click="selectEdition(edition)"
        :class="{'is-selected': selectedEdition && selectedEdition.id == edition.id}">
        <picture>
          <img :src="edition.picture" :alt="edition.title"/>
        </picture>

        <h2>{{edition.title}} <span>#{{ edition.issues + 1 }}</span></h2>
        <p>In <strong>4 hours</strong> with <strong>3 posts</strong>.</p>
        <span class="backlog" v-tooltip.top="'Posts in consideration'">12</span>
      </editor-editions--nav-item>
    </nav>

    <editor-editions--board>
      <edition-backlog v-if="selectedEdition" :edition="selectedEdition" />
    </editor-editions--board>

    <portal to="modal" v-if="isCreateEditionOpen">
      <create-edition :onClose="closeModal"></create-edition>
    </portal>
  </editor-editions-view>
</template>


<script>
import { mapState, mapGetters } from 'vuex'

import * as api from '@/api'

import EditionWidget from '@/components/widgets/EditionWidget'
import CreateEdition from '@/components/editor/CreateEdition'
import EditionBacklog from '@/components/editor/EditionBacklog'

export default {
  name: 'AuthorDetail',
  components: {
    EditionWidget,
    CreateEdition,
    EditionBacklog
  },

  data() {
    return {
      loadingProfile: true,
      author: null,
      topic: null,
      editionIds: [],
      cursor: null,
      isCreateEditionOpen: false,
      selectedEdition: null
    }
  },

  computed: {
    ...mapGetters({
      editions: 'allEditions'
    }),

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
    selectEdition(edition) {
      this.selectedEdition = edition

      console.log(this.selectedEdition.title)
    },

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
        this.selectedEdition = resp.editions[0]
        this.loadingProfile = false
        this.topics = resp.topics
      })
    }
  },

  created() {
    this.loadData()
    this.$store.dispatch('getEditions')
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

  &.is-selected
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
