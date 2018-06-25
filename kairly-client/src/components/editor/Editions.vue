<template>
  <editor-editions-view>
    <editor-editions--header>
      <h1>{{ selectedEdition.title }}</h1>

      <button-icon role="button" class="dropdown" @click="isSelectEditionOpen = !isSelectEditionOpen"></button-icon>

      <editor-editions--header--dropdown
        v-if="isSelectEditionOpen"
        v-on-clickaway="() => isSelectEditionOpen = false">
        <div
          v-for="edition in editions"
          :key="edition.id"
          :class="{'is-selected': selectedEdition && selectedEdition.id == edition.id}"
          @click="selectEdition(edition)">
          <h3>{{ edition.title }}</h3>
          <p>
            <strong>#{{ edition.issues + 1 }}</strong> is realising in
            <strong>4 hours</strong> with
            <strong>3 posts</strong>.
          </p>
        </div>
      </editor-editions--header--dropdown>

      <div class="create-edition">
        <a href="" @click.prevent="confirmDeleteEdition">Delete edition</a>
        <a href="" @click.prevent="isCreateEditionOpen = true">Start new edition</a>
      </div>
    </editor-editions--header>

    <editor-editions--board>
      <edition-backlog v-if="selectedEdition" :edition="selectedEdition" />
    </editor-editions--board>

    <portal to="modal" v-if="isCreateEditionOpen">
      <create-edition :onClose="closeModal"></create-edition>
    </portal>
  </editor-editions-view>
</template>


<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapGetters } from 'vuex'

import * as api from '@/api'

import EditionWidget from '@/components/widgets/EditionWidget'
import CreateEdition from '@/components/editor/CreateEdition'
import EditionBacklog from '@/components/editor/EditionBacklog'

export default {
  name: 'Editions',
  components: {
    EditionWidget,
    CreateEdition,
    EditionBacklog
  },

   directives: {
    onClickaway
  },

  data() {
    return {
      loadingProfile: true,
      author: null,
      topic: null,
      editionIds: [],
      cursor: null,
      isCreateEditionOpen: false,
      isSelectEditionOpen: false,
      selectedEdition: null
    }
  },

  computed: {

    editions() {
      const ids = this.editionIds
      return ids.map(id => this.$store.getters.edition(id))
    },

    canCreateEdition() {
      return this.author && this.user.id == this.author.id
    },

    ...mapGetters(['user'])
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

    confirmDeleteEdition() {
      if (window.confirm("Are you sure?")) {
        this.deleteEdition(this.selectedEdition)
      }
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
    position: relative

    display: block
    padding: $baseline 0

    h1
      display: inline-block
      margin-right: $baseline / 2

      font-family: $ff-serif
      font-size: $fs-2
      font-weight: 600

    button-icon
      display: inline-block
      border-radius: 100%
      height: $baseline * 1.25
      width: $baseline * 1.25

      cursor: pointer
      line-height: $baseline * 1.25
      text-align: center

      &:focus,
      &:hover
        background: #eee

      &::before
        content: $fa-var-chevron-down

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
        margin-left: $baseline / 4

        font-family: $ff-sans
        line-height: $baseline * 1.5

editor-editions--header--dropdown
  position: absolute
  left: 0
  top: $baseline * 2.5
  z-index: 1

  display: block
  width: 300px

  background: #fff
  border-radius: $baseline / 4
  overflow: hidden

  font-size: $fs--1

  //- item
  > div
    margin-bottom: $baseline / 4
    padding: 0 $baseline / 4

    cursor: pointer

    &:focus,
    &:hover
      background: #f5f5f5

    &:last-of-type
      margin-bottom: 0

  h3
    font-weight: 600

  p
    color: #777

    font-size: $fs--2



editor-editions--board



</style>
