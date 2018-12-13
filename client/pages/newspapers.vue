<template>
  <app-layout :name="$t('Manage newspapers')">
    <editor-newspapers-view>
      <editor-newspapers--empty
        v-if="newspapers.length === 0">

        <h1>{{ $t('Start your first newspaper!') }}</h1>

        <p>
          {{ $t("Are you interested in specific topic? Found a newspaper and start providing selection of best articles and tweets to others.") }}
        </p>

        <a href="" @click.prevent="isCreateNewspaperOpen = true">{{ $t('Start a newspaper') }}</a>
      </editor-newspapers--empty>

      <template v-else>
        <editor-newspapers--header>
          <div class="create-newspaper">
            <a href="" @click.prevent="isCreateNewspaperOpen = true">{{ $t('Start a newspaper') }}</a>
          </div>

          <div class="title">
            <h1 v-if="selectedNewspaper">{{ selectedNewspaper.title }}</h1>

            <button-icon
              v-if="selectedNewspaper"
              role="button"
              tabindex="0" class="dropdown"
              @click="isSelectNewspaperOpen = !isSelectNewspaperOpen">
            </button-icon>

            <editor-newspapers--header--dropdown
              v-if="isSelectNewspaperOpen"
              v-on-clickaway="() => isSelectNewspaperOpen = false">
              <div
                v-for="newspaper in newspapers"
                :key="newspaper.fullName"
                :class="{'is-selected': selectedNewspaper && selectedNewspaper.fullName == newspaper.fullName}"
                @click="selectNewspaper(newspaper)">
                <img :src="newspaper.picture" :alt="newspaper.title"/>
                <h3>{{ newspaper.title }}</h3>
                <p>
                  <strong>#{{ newspaper.issues + 1 }}</strong> {{ $t('is releasing in') }}
                  <strong>{{ timeFrom(newspaper.nextRelease) }}</strong> {{ $t('with') }}
                  <strong>{{ publishedPostCount(newspaper) }} {{ $t('posts') }}</strong>.
                </p>
              </div>
            </editor-newspapers--header--dropdown>
          </div>

          <div class="newspaper-controls" v-if="selectedNewspaper">
            <button-icon
              class="edit"
              role="button"
              tabindex="0"
              :title="$t('Edit newspaper')"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              @click="newspaperToEdit = selectedNewspaper">
            </button-icon>

            <button-icon
              class="delete"
              role="button"
              tabindex="0"
              :title="$t('Delete newspaper')"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              @click.prevent="confirmDeleteNewspaper">
            </button-icon>
          </div>

          <div class="mobile-menu">
            <button-icon
              class="menu"
              tabindex="0"
              role="button"
              :class="{'is-active': isMobileMenuOpen}"
              aria-label="Context menu"
              @click="isMobileMenuOpen = !isMobileMenuOpen">
            </button-icon>

            <div
              class="mobile-menu--dropdown"
              v-if="isMobileMenuOpen"
              v-on-clickaway="() => isMobileMenuOpen = false">
              <ul>
                <li><a href="" @click.prevent="isCreateNewspaperOpen = true">{{ $t('Start new newspaper') }}</a></li>
                <li><a href="" @click.prevent="newspaperToEdit = selectedNewspaper">{{ $t('Edit newspaper') }}</a></li>
                <li><a href="" @click.prevent="confirmDeleteNewspaper">{{ $t('Delete newspaper') }}</a></li>
              </ul>
            </div>
          </div>
        </editor-newspapers--header>

        <editor-newspapers--mobile-switcher>
          <nav>
            <a
              href=""
              :class="{'is-active': mobileSwitcher == 1}"
              @click.prevent="mobileSwitcher = 1">
              {{ $t('Upcoming issue') }}
            </a>

            <a
              href=""
              :class="{'is-active': mobileSwitcher == 2}"
              @click.prevent="mobileSwitcher = 2">
              {{ $t('Considered posts') }}
            </a>
          </nav>
        </editor-newspapers--mobile-switcher>

        <editor-newspapers--board v-if="isBacklogLoaded"
          :class="{'upcoming-issue': mobileSwitcher == 1, 'backlog': mobileSwitcher ==2}"
        >
          <newspaper-backlog v-if="selectedNewspaper"
            :newspaper="selectedNewspaper"
            :backlog="postsBacklog"
            :published="postsPublished"
          />
        </editor-newspapers--board>
        <loading-spinner v-else />
      </template>

      <portal to="modal" v-if="isCreateNewspaperOpen">
        <edit-newspaper :closeModal="closeModal" :onCreated="newNewspaperCreated"></edit-newspaper>
      </portal>

      <portal to="modal" v-if="newspaperToEdit">
        <edit-newspaper :closeModal="closeModal" :newspaper="newspaperToEdit"></edit-newspaper>
      </portal>
    </editor-newspapers-view>
  </app-layout>
</template>


<script>
import moment from 'moment'

import { directive as onClickaway } from '@/lib/vue-clickaway'
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import EditNewspaper from '@/components/editor/EditNewspaper'
import NewspaperBacklog from '@/components/editor/NewspaperBacklog'

export default {
  name: 'Newspapers',

  head() {
    return {
      title: this.selectedNewspaper ? this.selectedNewspaper.title : 'My Newspapers – Kairly'
    }
  },

  components: {
    AppLayout,
    EditNewspaper,
    NewspaperWidget,
    NewspaperBacklog
  },

  directives: {
    onClickaway
  },

  data() {
    return {
      isCreateNewspaperOpen: false,
      isSelectNewspaperOpen: false,
      isMobileMenuOpen: false,
      mobileSwitcher: 1,
      newspaperToEdit: null,

      selectedFullName: null, // keep just fullName instead fill object to get fresh data on change
      isBacklogLoaded: false,
      postsBacklog: [],
      postsPublished: []
    }
  },

  computed: {
    newspapers() {
      const ids = this.$store.state.auth.user.newspapers.map(newspaper => newspaper.fullName)
      const newspapers = ids.map(id => this.$store.getters.newspaper(id))
      newspapers.sort(({nextRelease: a}, {nextRelease: b}) => a < b ? -1 : (a > b ? 1 : 0))
      return newspapers
    },

    selectedNewspaper() {
      if (!this.selectedFullName || !this.newspapers) return null
      return this.newspapers.find(n => n.fullName === this.selectedFullName)
    },

    ...mapState({
      backlog: state => state.backlog,
      user: state => state.auth.user
    })
  },

  methods: {
    timeFrom(dt) {
      return moment(dt).from()
    },

    publishedPostCount(newspaper) {
      let count = 0
      Object.keys(this.backlog).forEach(postId => {
        if (this.backlog[postId][newspaper.fullName] === 'P') {
          count++
        }
      })
      return count
    },

    async selectNewspaper(newspaper) {
      this.isSelectNewspaperOpen = false

      if (!newspaper) {
        this.selectedFullName = null
        this.postsBacklog = []
        this.postsPublished = []
        return
      }

      const { fullName } = newspaper
      this.selectedFullName = fullName

      this.isBacklogLoaded = false
      const { backlog, publish } = await this.$axios.$get(`/newspapers/${fullName}/backlog`)
      this.postsBacklog = backlog
      this.postsPublished = publish
      this.isBacklogLoaded = true
    },

    confirmDeleteNewspaper() {
      if (window.confirm("Are you sure?")) {
        const { fullName } = this.selectedNewspaper
        this.deleteNewspaper(this.selectedNewspaper)

        if (this.newspapers.length) {
          this.selectNewspaper(this.newspapers.find(e => e.fullName !== fullName))
        } else {
          this.selectNewspaper(null)
        }
      }
    },

    closeModal() {
      this.isCreateNewspaperOpen = false
      this.newspaperToEdit = null
    },

    newNewspaperCreated(newspaper) {
      this.selectNewspaper(newspaper)
    },

    ...mapActions(['deleteNewspaper'])
  },

  async fetch({ store, redirect }) {
    const { user } = store.state.auth

    await store.dispatch('getUserBacklog')

    const newspaperIds = user.newspapers.map(newspaper => newspaper.fullName)
    await store.dispatch('getNewspapers', newspaperIds)
  },

  created() {
    if (this.newspapers.length) {
      this.selectNewspaper(this.newspapers[0])
    }
  },
}
</script>

<style lang="sass">
editor-newspapers--empty
  display: block
  max-width: 600px
  margin: $baseline auto
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  > h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  > p
    margin-bottom: $baseline

  > a
    +subscribed-button

    display: inline-block

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

editor-newspapers-view
  position: relative

  display: block
  padding: 0 $baseline
  max-width: 1600px
  margin: 0 auto

  @media (max-width: $mobile)
    padding: 0 $baseline/4


  //- Header
  editor-newspapers--header
    position: relative

    display: grid
    grid-template-columns: 2fr auto 2fr
    padding: $baseline 0
    text-align: center

    @media (max-width: 800px)
      grid-template-columns: 1fr auto
      padding: $baseline/2 0

      text-align: left


    //- Newspaper Title
    .title

      h1
        display: inline-block
        margin-right: $baseline / 2

        font-family: $ff-serif
        font-size: $fs-4
        font-weight: 600
        line-height: $baseline * 2
        vertical-align: middle
        text-align: center
        text-shadow: 0 0 5px #fafafa

        @media (max-width: $mobile)
          margin-right: 0
          font-size: $fs-3


      > button-icon
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

    .create-newspaper
      align-self: center
      justify-self: start

      @media (max-width: 800px)
        display: none

      a
        +subscribe-button

        display: inline-block
        height: $baseline * 1.5
        border-radius: $baseline * 0.75
        padding: 0 $baseline/2
        margin-left: $baseline / 4

        font-family: $ff-sans
        line-height: $baseline * 1.5

    .newspaper-controls
      align-self: center
      justify-self: end

      @media (max-width: 800px)
        display: none

      > button-icon
        display: inline-block
        border-radius: 100%
        height: $baseline * 1.25
        margin-left: $baseline / 4
        width: $baseline * 1.25

        background: #fff

        cursor: pointer
        line-height: $baseline * 1.25
        text-align: center

        &:focus,
        &:hover
          background: #eee

        &.edit::before
          content: $fa-var-pencil

        &.delete::before
          content: $fa-var-trash

    .mobile-menu
      display: none
      align-self: center


      @media (max-width: 800px)
        display: block

      > button-icon
        display: inline-block
        border-radius: 100%
        height: $baseline * 1.25
        width: $baseline * 1.25

        cursor: pointer
        line-height: $baseline * 1.25
        text-align: center

        &:focus,
        &:hover,
        &.is-active
          background: #eee

      .mobile-menu--dropdown
        position: absolute
        right: 0
        top: $baseline * 2.5
        z-index: 100

        display: block

        +blur
        +box-shadow

        font-size: $fs--1
        text-align: left

        a
          display: block
          padding: $baseline/4

          color: #000

          &:focus,
          &:hover
            background: #fff


editor-newspapers--header--dropdown
  position: absolute
  left: 50%
  top: $baseline * 3
  z-index: 1

  display: block
  margin-left: -200px
  width: 400px

  +blur(10px)
  +box-shadow

  font-size: $fs--1

  @media (max-width: $mobile)
    left: $baseline / 2
    right: $baseline / 2
    top: $baseline * 2.5

    margin-left: 0
    width: auto

  //- item
  > div
    display: grid
    grid-template-areas: "newspaper-dd-picture newspaper-dd-title" "newspaper-dd-picture newspaper-dd-info"
    grid-template-columns: $baseline*3 auto
    grid-column-gap: $baseline / 2
    padding: $baseline / 2

    border-bottom: 1px solid #eee

    cursor: pointer
    text-align: left

    &:focus,
    &:hover
      background: #fff

    &:last-of-type
      margin-bottom: 0

      border-bottom: 0

  //- newspaper cover
  img
    grid-area: newspaper-dd-picture
    height: $baseline * 2
    width: 100%

    object-fit: cover


  //- newspaper title
  h3
    grid-area: newspaper-dd-title
    font-weight: 600

  //- information about next issue
  p
    grid-area: newspaper-dd-info
    color: #777

    font-size: $fs--1


//- Mobile switcher (upcoming release, considered posts)
editor-newspapers--mobile-switcher
  display: none

  @media (max-width: 1260px)
    display: block

  nav
    margin-bottom: $baseline / 2

    font-size: $fs-2

    a
      display: inline-block
      margin-right: $baseline/2

      color: $c-base

      font-weight: 500

      &:last-of-type
        margin-right: 0

      &.is-active
        color: #000

// Board
editor-newspapers--board
  @media (max-width: 1260px)
    newspaper-backlog--info
      display: none

    newspaper-backlog-view > div
        grid-template-columns: 1fr

    //- if upcoming issue is opened
    &.upcoming-issue
      newspaper-backlog--backlog
        display: none

    //- if backlog is opened
    &.backlog
      newspaper-backlog--next-issue
        display: none


</style>
