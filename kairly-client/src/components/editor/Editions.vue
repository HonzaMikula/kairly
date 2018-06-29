<template>
  <app-layout>
    <editor-editions-view>
      <editor-editions--header>
        <h1 v-if="selectedEdition">{{ selectedEdition.title }}</h1>

        <button-icon v-if="selectedEdition" role="button" class="dropdown" @click="isSelectEditionOpen = !isSelectEditionOpen"></button-icon>

        <editor-editions--header--dropdown
          v-if="isSelectEditionOpen"
          v-on-clickaway="() => isSelectEditionOpen = false">
          <div
            v-for="edition in editions"
            :key="edition.fullName"
            :class="{'is-selected': selectedEdition && selectedEdition.fullName == edition.fullName}"
            @click="selectEdition(edition)">
            <img :src="edition.picture" :alt="edition.title"/>
            <h3>{{ edition.title }}</h3>
            <p>
              <strong>#{{ edition.issues + 1 }}</strong> is releasing in
              <strong>4 hours</strong> with
              <strong>3 posts</strong>.
            </p>
          </div>
        </editor-editions--header--dropdown>

        <div class="create-edition">
          <a v-if="selectedEdition" href="" @click.prevent="confirmDeleteEdition">Delete edition</a>
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
  </app-layout>
</template>


<script>
import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapActions, mapGetters } from 'vuex'

import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import EditionWidget from '@/components/widgets/EditionWidget'
import CreateEdition from '@/components/editor/CreateEdition'
import EditionBacklog from '@/components/editor/EditionBacklog'

export default {
  name: 'Editions',

  metaInfo() {
    return {
      title: this.selectedEdition ? this.selectedEdition.title : 'My Editions'
    }
  },

  components: {
    AppLayout,
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
        this.loadData()
      }
    },

    closeModal() {
      this.isCreateEditionOpen = false
      this.loadData()
    },

    loadData() {
      this.loadingProfile = true
      this.loadingPosts = true
      this.author = null
      this.editionIds = []
      this.posts = []
      this.cursor = null

      api.getAuthorDetail(this.user.id).then(resp => {
        resp.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
        this.author = resp.author
        this.editionIds = resp.editions.map(e => e.fullName)
        this.selectedEdition = resp.editions[0]
        this.loadingProfile = false
        this.topics = resp.topics
      })
    },

    ...mapActions(['deleteEdition'])
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
  max-width: 1600px

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
  height: $baseline * 10
  width: 380px

  backdrop-filter: blur(10px) saturate(125%)
  border-radius: $baseline / 4

  font-size: $fs--1

  //- item
  > div
    padding: $baseline / 2

    border-bottom: 1px solid #eee

    cursor: pointer

    &:focus,
    &:hover
      background: #fff

    &:last-of-type
      margin-bottom: 0

      border-bottom: 0

  //- edition cover
  img
    float: left
    margin-right: $baseline / 2
    height: $baseline * 2
    width: $baseline * 3

  //- edition title
  h3
    font-weight: 600

  //- information about next issue
  p
    color: #777

    font-size: $fs--2



editor-editions--board



</style>
