<template>
  <app-layout :name="$t('Newspaper detail')">
    <div class="newspaper-detail" itemtype="https://bib.schema.org/Newspaper" itemscope>
      <header class="newspaper-detail--header">
        <h1 itemprop="name"><nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">{{ newspaper.title }}</nuxt-link></h1>
        <p>{{ newspaper.description }}</p>

        <picture itemprop="image">
          <img v-if="newspaper.picture" :src="newspaper.picture" :alt="newspaper.title"/>
          <div v-else class="image-placeholder"></div>
        </picture>

        <div class="newspaper-detail--subscribe" v-if="loggedIn">
          <newspaper-subscription :newspaper="newspaper" />

          <p>{{ periodicity }}</p>
        </div>
      </header>

      <div class="newspaper-detail--info">
        <ul>
          <li>{{ periodicity }}</li>
          <li class="issues">#{{ newspaper.issues }}</li>
          <li>{{ newspaper.likes }} {{ $t('readers') }}</li>
          <li>{{ newspaper.editor.name }}</li>
          <li class="price">{{ newspaper.price.split('.')[0] }} Kč měsíčně</li>
        </ul>
      </div>

      <template v-if="issue">
        <nav class="newspaper-detail--navigation">
          <nuxt-link
            v-if="links.prev"
            :to="links.prev"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="$t('Previous issue')"
            class="previous"
          ></nuxt-link>

          <nuxt-link
            v-if="links.next"
            :to="links.next"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="$t('Next issue')"
            class="next"
          ></nuxt-link>
        </nav>

        <div class="newspaper-detail--issue">
          <Issue :issue="issue" :subscription="newspaper.subscription" :hideDate="true">
            <template slot="newspaperTitle">{{ $t('Issue from') }} {{ issue.time | moment('D. M. YYYY')}}</template>
          </Issue>
        </div>

        <footer class="newspaper-detail--footer">
          <a
            :href="`https://www.facebook.com/sharer/sharer.php?u=https://kairly.com/${issue.id}`"
            target="_blank"
            class="share-fb">
            {{ $t('Share on Facebook') }}
          </a>

          <a
            :href="`https://twitter.com/intent/tweet?url=https://kairly.com/${issue.id}&text=${newspaper.title}`"
            target="_blank"
            class="share-twitter"
          >
            {{ $t('Share on Twitter') }}
          </a>
        </footer>
      </template>

      <div class="newspaper-detail--empty-newspaper" v-else>
        <h2>{{ $t('No issue yet') }}</h2>
        <p>
          {{ $t('Subscribe the newspaper and once it\'s published, we will show you on your timeline.') }}
        </p>
      </div>
    </div>

    <kairly-promo v-if="!loggedIn" />
  </app-layout>
</template>

<script>
/*
  Don't forget that
  /:author/:newspaper/:issue is also routed to this page
*/

import { mapState, mapMutations, mapActions } from 'vuex'

import { errorToParams } from '@/utils/errors'

import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'
import KairlyPromo from '@/components/KairlyPromo'

export default {
  name: 'NewspaperDetail',

  auth: false,

  head() {
    const { title, name, description, picture, editor} = this.newspaper
    return {
      title: `${title} – Kairly`,
      meta: [
        { hid: 'description', name: 'description', content: description },
        { hid: 'og:title', property: 'og:title', content: `${title} – Kairly` },
        { hid: 'og:description', property: 'og:description', content: description },
        { hid: 'og:image', property: 'og:image', content: picture },
        { hid: 'og:image:alt', property: 'og:image:alt', content: title },
        { hid: 'og:type', property: 'og:type', content: 'product' },
        { hid: 'og:url', property: 'og:url', content: `https://www.kairly.com/${editor.id}/${name}` },
        { hid: 'twitter:card', property: 'twitter:card', content: 'summary' },
        { hid: 'twitter:site', property: 'twitter:site', content: '@kairlyapp' },
        { hid: 'twitter:title', property: 'twitter:title', content: `${title} – Kairly` },
        { hid: 'twitter:description', property: 'twitter:description', content: description },
        { hid: 'twitter:image', property: 'twitter:image', content: picture },
      ]
    }
  },

  components: {
    AppLayout,
    Issue,
    NewspaperSubscription,
    KairlyPromo
  },

  mixins: [PeriodicityMixin],

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    isEditor() {
      if (this.newspaper) {
        const author = this.newspaper.editor
        return this.user.id === author.id
      } else {
        return false
      }
    },

    periodicity() {
      return this.getPeriodicityLabel(this.newspaper.periodicity)
    },

    ...mapState({
      user: state => state.auth.user
    })
  },

  async asyncData({ store, params, error }) {
    const fullName = `${params.author}/${params.newspaper}`

    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }

    try {
      const { newspaper, issue, links } = await store.dispatch('getNewspaperDetail', {
        newspaperId: fullName,
        issue: params.issue
      })
      return { newspaper, issue, links }
    } catch (err) {
      error(errorToParams(err))
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.newspaper-detail
  position: relative

  margin: 0 auto
  max-width: 900px
  padding-bottom: $baseline


//- Header
.newspaper-detail--header
  position: sticky
  top: -1px
  z-index: 5

  display: grid
  grid-column-gap: $baseline / 2
  grid-template-areas: "issue-header-image issue-header-title issue-header-subscription" "issue-header-image issue-header-description issue-header-subscription"
  grid-template-columns: $baseline*7 auto $baseline*7
  grid-template-rows: $baseline*2 auto
  padding: $baseline/4 0
  margin: $baseline*0.75 0
  overflow: hidden

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: 850px)
    grid-template-areas: "issue-header-title issue-header-subscription" "issue-header-description issue-header-subscription"
    grid-template-columns: auto $baseline*7
    padding-left: $baseline / 2

  @media (max-width: $mobile)
    position: static

    grid-template-areas: "issue-header-title" "issue-header-description" "issue-header-subscription"
    grid-template-columns: 100%

    padding-bottom: 0
    margin: 0

    backdrop-filter: none

  //- Title
  h1
    grid-area: issue-header-title

    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center
    text-shadow: 0 0 5px #fafafa

    @media (max-width: 850px)
      text-align: left

    @media (max-width: $mobile)
      font-size: $fs-3

    a
      color: #000

  //- Description
  p
    grid-area: issue-header-description

    text-align: center

    @media (max-width: 850px)
      text-align: left

  //- Picture
  > picture
    grid-area: issue-header-image

    @media (max-width: 850px)
      display: none

    img
      height: 100%
      width: 100%

      object-fit: cover


//- Subscribe
.newspaper-detail--subscribe
  grid-area: issue-header-subscription
  padding: $baseline/4 0

  text-align: center

  @media (max-width: $mobile)
    position: static

  .newspaper-subscription button.to-subscribe,
  .newspaper-subscription button.is-canceled
    +button(secondary, medium)
    padding: 0
    width: 100%

    @media (max-width: $mobile)
      padding: 0 $baseline/2
      width: auto

  .newspaper-subscription button.is-subscribed
    +button(primary, medium)
    padding: 0
    width: 100%

    @media (max-width: $mobile)
      padding: 0 $baseline/2
      width: auto

  > p
    color: #555

    font-family: $ff-sans
    font-size: $fs--1
    line-height: 1.42
    text-align: center

    @media (max-width: $mobile)
      display: none

//- Info row about newspaper
.newspaper-detail--info
  display: block
  padding: $baseline/4 0

  border-bottom: 1px solid #ddd
  border-top: 1px solid #ddd

  ul
    display: table
    margin: 0 auto

    @media (max-width: $mobile)
      padding: 0 $baseline/4

  li
    display: inline-block

    font-size: $fs--1
    font-family: $ff-serif
    vertical-align: middle

    &::after
      display: inline-block
      padding: 0 $baseline/2

      content: '•'

      @media (max-width: $mobile)
        padding: 0 $baseline/4

    &:last-of-type::after
      display: none

    @media (max-width: $mobile)
      &.issues,
      &.price
        display: none

      &:nth-of-type(4)::after
        display: none

//- Navigation between issues
.newspaper-detail--navigation
  display: grid
  grid-template-columns: auto 1fr auto
  grid-template-areas: "prev-link . next-link"
  padding-top: $baseline / 2
  margin-bottom: -($baseline * 2.375)

  a
    position: relative
    z-index: 3

    display: block
    border-radius: 100%
    height: $baseline * 1.5
    width: $baseline * 1.5

    background: #fff
    color: #000

    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: $c-base
      color: #fff

    &.is-disabled
      opacity: 0.5

      cursor: default
      pointer-events: none

      &:hover,
      &:focus
        background: #fff
        color: #000

    &::before
      +fa-icon()
      @extend .fas

    &.previous
      grid-area: prev-link

      &::before
        content: fa-content($fa-var-arrow-left)

    &.next
      grid-area: next-link

      &::before
        content: fa-content($fa-var-arrow-right)


//- Issue
.newspaper-detail--issue
  display: block

  timeline-newspaper
    margin-top: $baseline


//- Footer with social buttons
.newspaper-detail--footer
  text-align: center

  > a
    border-radius: 5px
    display: inline-block
    height: $baseline * 1.25
    margin-right: $baseline / 4
    margin-bottom: $baseline / 4
    padding: 0 $baseline/4

    background: #eee
    color: #000

    cursor: pointer
    font-size: $fs--1
    line-height: $baseline * 1.25
    vertical-align: middle

    &::before
      position: relative
      top: -1px

      margin-right: $baseline / 4
      vertical-align: middle

      font-size: $fs-1

    &:focus,
    &:hover
      background: #bbb
      color: #000

    &.share-fb::before
      +fa-icon()
      @extend .fab

      margin-right: 0

      font-size: $fs-1

      content: fa-content($fa-var-facebook-square)

    &.share-twitter::before
      +fa-icon()
      @extend .fab

      margin-right: 0

      font-size: $fs-1

      content: fa-content($fa-var-twitter)

.newspaper-detail--empty-newspaper
  display: block
  margin-top: $baseline * 2
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  h2
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600
</style>
