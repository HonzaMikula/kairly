<template>
  <AppLayout :name="$t('Manage newsletters')">
    <div class="newspaper-editor-view" @click="clearSelection()">
      <div
        v-if="newspapers.length === 0"
        class="newspaper-editor--empty"
      >
        <h1>{{ $t('Start your first newsletter!') }}</h1>

        <p>
          {{ $t("Are you interested in specific topic? Found a newsletter and start providing selection of best articles and tweets to others. Here is some inspiration:") }}

          <nuxt-link to="/janmikula/malostranskenoviny">Malostranský deník</nuxt-link>,
          <nuxt-link to="/janmikula/tydenik-skola-hrou">Týdeník škola hrou</nuxt-link> or
          <nuxt-link to="/janmikula/product-design-weekly">Product Design Newsletter</nuxt-link>.
        </p>

        <div class="newspaper-editor--empty--columns">
          <section>
            <h3>{{ $t('How to found a newsletter?') }}</h3>
            <ul>
              <li>{{ $t('Give it a name and description.') }}</li>
              <li>{{ $t('Choose when and how often newsletter will be published.') }}</li>
            </ul>

            <h3>{{ $t('What\'s your layout options?') }}</h3>
            <ul>
              <li>{{ $t('Newsletter can be split into sections.') }}</li>
              <li>{{ $t('You can use two or three column layouts.') }}</li>
            </ul>

            <picture>
              <img src="~assets/onboarding/manage-newsletter-3.png" alt="Illustration">
            </picture>
          </section>

          <section>
            <h3>{{ $t('How to add content to newsletter?') }}</h3>
            <ul>
              <li>{{ $t('Subscribe to authors and other newsletters.') }}</li>
              <li v-html="$t('Use <span class=\'fake-button\'></span> Consider button.')" />
              <li>{{ $t('Or add external articles or tweets simply by pasting URL.') }}</li>
            </ul>

            <picture>
              <img src="~assets/onboarding/manage-newsletter-2.png" alt="Illustration">
            </picture>
          </section>
        </div>

        <nuxt-link to="/newspapers/start">{{ $t('Start newsletter') }}</nuxt-link>
      </div>

      <template v-else>
        <header class="newspaper-editor--header">
          <div class="title">
            <h1
              v-if="selectedNewspaper"
              @click="isSelectNewspaperOpen = !isSelectNewspaperOpen"
            >
              {{ selectedNewspaper.title }}
            </h1>

            <button-icon
              v-if="selectedNewspaper"
              class="dropdown"
              role="button"
              tabindex="0"
              @click="isSelectNewspaperOpen = !isSelectNewspaperOpen"
            />

            <div
              v-if="isSelectNewspaperOpen"
              v-on-clickaway="() => isSelectNewspaperOpen = false"
              class="newspaper-editor--header--dropdown"
            >
              <div
                v-for="newspaper in newspapers"
                :key="newspaper.fullName"
                :class="{'is-selected': selectedNewspaper && selectedNewspaper.fullName == newspaper.fullName}"
                @click="selectNewspaper(newspaper)"
              >
                <img v-if="newspaper.picture" :src="newspaper.picture" :alt="newspaper.title">
                <div v-else class="image-placeholder" />
                <h3>{{ newspaper.title }}</h3>
                <p>
                  <strong>#{{ newspaper.issues + 1 }}</strong> {{ $t('is releasing in') }}
                  <strong>{{ timeFrom(newspaper.nextRelease) }}</strong> {{ $t('with') }}
                  <strong>{{ publishedPostCount(newspaper) }} {{ $t('posts') }}</strong>.
                </p>
              </div>
            </div>
          </div>

          <div v-if="selectedNewspaper" class="newspaper-controls">
            <nuxt-link
              v-b-tooltip
              class="detail"
              :to="{name: 'author-newspaper', params: {author: selectedNewspaper.editor.id, newspaper: selectedNewspaper.name}}"
              :title="$t('Go to newsletter detail')"
            />

            <nuxt-link
              v-if="selectedNewspaper.editor.id === user.id"
              v-b-tooltip
              class="settings"
              :to="{name: 'author-newspaper-settings', params: {author: selectedNewspaper.editor.id, newspaper: selectedNewspaper.name}}"
              :title="$t('Edit newsletter')"
            />
          </div>

          <div class="mobile-menu">
            <button-icon
              class="menu"
              tabindex="0"
              role="button"
              :class="{'is-active': isMobileMenuOpen}"
              aria-label="Context menu"
              @click="isMobileMenuOpen = !isMobileMenuOpen"
            />

            <div
              v-if="isMobileMenuOpen"
              v-on-clickaway="() => isMobileMenuOpen = false"
              class="mobile-menu--dropdown"
            >
              <ul>
                <li>
                  <nuxt-link
                    :to="{name: 'author-newspaper', params: {author: selectedNewspaper.editor.id, newspaper: selectedNewspaper.name}}"
                  >
                    {{ $t('Newsletter detail') }}
                  </nuxt-link>
                </li>
                <li v-if="selectedNewspaper.editor.id === user.id">
                  <nuxt-link
                    :to="{name: 'author-newspaper-settings', params: {author: selectedNewspaper.editor.id, newspaper: selectedNewspaper.name}}"
                  >
                    {{ $t('Edit newsletter') }}
                  </nuxt-link>
                </li>
              </ul>
            </div>
          </div>
        </header>

        <div
          v-if="isBacklogLoaded"
          class="editor-newspapers--board upcoming-issue"
        >
          <NewspaperBacklog
            v-if="selectedNewspaper"
            :newspaper="selectedNewspaper"
          />
        </div>
        <loading-spinner v-else />
      </template>
    </div>
  </AppLayout>
</template>

<script>
import moment from 'moment'

import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import NewspaperBacklog from '@/components/editor/backlog/NewspaperBacklog'
import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'Newspapers',

  components: {
    AppLayout,
    NewspaperBacklog
  },

  mixins: [ErrorHandler],

  data () {
    return {
      isSelectNewspaperOpen: false,
      isMobileMenuOpen: false,
      externalLink: null,
      selectedFullName: null, // keep just fullName instead fill object to get fresh data on change
      isBacklogLoaded: false,
    }
  },

  async fetch ({ store, redirect }) {
    const { user } = store.state.auth

    await store.dispatch('backlog/loadUserBacklog')

    const newspaperIds = user.newspapers.map(newspaper => newspaper.fullName)
    await store.dispatch('getNewspapers', newspaperIds)
  },

  head () {
    return {
      title: this.selectedNewspaper ? this.selectedNewspaper.title : 'My Newsletters – Kairly'
    }
  },

  computed: {
    isAdmin () {
      const { user } = this.$store.state.auth
      return user.isAdmin
    },

    newspapers () {
      const ids = this.$store.state.auth.user.newspapers.map(newspaper => newspaper.fullName)
      const newspapers = ids.map(id => this.$store.getters['entities/getNewspaper'](id))
      newspapers.sort(({ nextRelease: a }, { nextRelease: b }) => a < b ? -1 : (a > b ? 1 : 0))
      return newspapers
    },

    selectedNewspaper () {
      if (!this.selectedFullName || !this.newspapers) { return null }
      return this.newspapers.find(n => n.fullName === this.selectedFullName)
    },

    ...mapState({
      backlog: state => state.backlog.userBacklog,
      user: state => state.auth.user
    })
  },

  mounted () {
    // do select in mounted() to do it only on client side (no SSR)
    if (this.newspapers.length) {
      let selectedNewspaper = null
      const selectedFullName = window.localStorage.getItem('manageNewspapers.selected')
      selectedNewspaper = this.newspapers.find(n => n.fullName === selectedFullName)
      this.selectNewspaper(selectedNewspaper || this.newspapers[0])
    }
  },

  methods: {
    timeFrom (dt) {
      return moment(dt).from()
    },

    clearSelection () {
      this.$store.commit('backlog/cleanSelection')
    },

    publishedPostCount (newspaper) {
      let count = 0
      Object.keys(this.backlog).forEach(postId => {
        if (this.backlog[postId][newspaper.fullName] === 'P') {
          count++
        }
      })
      return count
    },

    async selectNewspaper (newspaper) {
      this.isSelectNewspaperOpen = false

      if (!newspaper) {
        this.selectedFullName = null
        return
      }

      const { fullName } = newspaper
      this.selectedFullName = fullName
      this.$store.commit('backlog/cleanSelection')

      this.isBacklogLoaded = false
      await this.loadNewspaperBacklog(fullName)
      this.isBacklogLoaded = true

      if (process.client) {
        window.localStorage.setItem('manageNewspapers.selected', fullName)
      }
    },

    closeModal () {
      this.isCreateNewspaperOpen = false
    },

    newNewspaperCreated (newspaper) {
      this.selectNewspaper(newspaper)
    },

    ...mapActions({
      deleteNewspaper: 'deleteNewspaper',
      loadNewspaperBacklog: 'backlog/loadNewspaperBacklog',
      addToBacklog: 'backlog/add',
    }),
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'
@import './styles/components/mixins'

.newspaper-editor-view
  position: relative

  display: block
  padding: 0 $baseline

  @media (max-width: $mobile)
    padding: 0 $baseline/4

  //- Header
  .newspaper-editor--header
    position: relative

    display: grid
    grid-template-columns: auto 2fr
    max-width: 900px
    margin: 0 auto
    padding: $baseline/2 0

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

        cursor: pointer
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

        a
          color: #000

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
          content: fa-content($fa-var-chevron-down)

    .newspaper-controls
      display: flex
      align-self: center
      justify-self: end

      @media (max-width: 800px)
        display: none

      > button-icon,
      > a
        display: inline-block
        border-radius: 100%
        height: $baseline * 1.25
        margin-left: $baseline / 4
        width: $baseline * 1.25

        background: #fff
        color: #000

        cursor: pointer
        line-height: $baseline * 1.25
        text-align: center

        &:focus,
        &:hover
          background: #eee

        &.detail::before
          +fa-icon()
          @extend .fas
          content: fa-content($fa-var-info-circle)

        &.settings::before
          +fa-icon()
          @extend .fas
          content: fa-content($fa-var-cog)

        &.edit::before
          content: fa-content($fa-var-pencil-alt)

        &.delete::before
          content: fa-content($fa-var-trash)

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

//- When there is no posts
.newspaper-editor--empty
  display: block
  max-width: 900px
  margin: $baseline auto
  padding: $baseline

  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600
    text-align: center

  h1 + p,
  h1 + p + p
    margin-bottom: $baseline

    a
      color: $c-base

      font-weight: 600
      text-decoration: underline

      &:hover,
      &:focus
        text-decoration: none

  section:first-of-type
    margin-bottom: $baseline

  section
    img
      border: 1px solid #eee
      box-shadow: 0 0 $baseline/2 #ccc
      max-width: 100%

  h3
    margin-bottom: $baseline / 4
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

  h3 + p
    margin-bottom: auto

  ul,
  ol
    margin-bottom: $baseline

    li
      list-style: disc outside
      margin-bottom: $baseline / 4
      margin-left: $baseline * 0.75

      line-height: 1.42

      a
        color: darken($c-base, 10%)

        font-weight: 600

        &:hover,
        &:focus
          color: darken($c-base, 20%)

  ol li
    list-style: decimal outside

  .fake-button
    +button-icon($fa-var-newspaper)

    cursor: auto

  //- Start a newsletter button
  > a
    +button(primary, large)
    margin: $baseline auto 0 auto
    display: table

.newspaper-editor--empty--columns
  display: grid
  grid-template-columns: 1fr 1fr
  grid-column-gap: $baseline

  @media (max-width: $mobile)
    grid-template-columns: auto

.newspaper-editor--header--dropdown
  position: absolute
  left: 0
  top: $baseline * 3
  z-index: 100

  display: block
  padding: $baseline/4 0
  width: 400px

  +blur(30px)
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
    padding: $baseline / 4 $baseline/2

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

  .image-placeholder
    grid-area: newspaper-dd-picture
    height: $baseline * 2
    background-image: radial-gradient(#fafafa, #aaa)

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
.newspaper-editor--mobile-switcher
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

      font-weight: 600

      &:last-of-type
        margin-right: 0

      &.is-active
        color: #000

.editor-newspapers--board
  max-width: 900px
  margin-left: $baseline

  @media (max-width: 1260px)
    margin-left: 0
</style>
