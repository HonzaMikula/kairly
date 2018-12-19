<template>
  <app-layout :name="$t('Newspaper detail')">
    <newspaper-detail-view itemtype="https://bib.schema.org/Newspaper" itemscope>
      <newspaper-detail--header>
        <h1 itemprop="name">{{ newspaper.title }}</h1>
        <p>{{ newspaper.description }}</p>

        <newspaper-detail--subscribe v-if="loggedIn">
          <newspaper-subscription :newspaper="newspaper" />

          <p>{{ periodicity }}</p>
        </newspaper-detail--subscribe>
      </newspaper-detail--header>

      <div>
        <newspaper-detail--info>
          <ul>
            <li>{{ periodicity }}</li>

            <li>#{{ newspaper.issues }}</li>

            <li>{{ newspaper.likes }} {{ $t('readers') }}</li>

            <li>10 CZK / month</li>
          </ul>
        </newspaper-detail--info>
      </div>

      <newspaper-detail--last-newspaper>
        <Issue :issue="issues[0]" :subscription="newspaper.subscription" :hideDate="true">
          <template slot="newspaperTitle">{{ $t('Issue from') }} {{ issues[0].time | moment('D. M. YYYY')}}</template>
        </Issue>
      </newspaper-detail--last-newspaper>

      <newspaper-detail--empty-newspaper v-if="issues.length === 0">
        <h2>{{ $t('No issue yet') }}</h2>

        <p>
          {{ $t('Subscribe the newspaper and once it\'s published, we will show you on your timeline.') }}
        </p>
      </newspaper-detail--empty-newspaper>

      <div class="newspaper-detail--footer">
        <picture itemprop="image">
          <img v-if="newspaper.picture" :src="newspaper.picture" :alt="newspaper.title"/>
          <div v-else class="image-placeholder"></div>
        </picture>
      </div>
    </newspaper-detail-view>
  </app-layout>
</template>


<script>
import { mapState, mapMutations, mapActions } from 'vuex'

import { errorToParams } from '@/utils/errors'

import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'

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
    NewspaperSubscription
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
      const { newspaper, issues } = await store.dispatch('getNewspaperDetail', { newspaperId: fullName })
      return { newspaper, issues }
    } catch (err) {
      error(errorToParams(err))
    }
  }
}
</script>

<style lang="sass">
newspaper-detail-view
  position: relative

  display: block
  margin: 0 auto
  max-width: 900px
  padding-bottom: $baseline

//- Header
.newspaper-detail--footer
  padding-top: $baseline / 2

  border-top: 1px solid #ddd
  img
    width: 100%
    max-height: 400px

    object-fit: cover

//- Header
newspaper-detail--header
  position: sticky
  top: -1px
  z-index: 1

  display: block
  padding: $baseline/4 $baseline
  margin: $baseline*0.75 0
  overflow: hidden

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: $mobile)
    position: static
    padding-bottom: 0
    margin: 0

  //- Title
  h1
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center
    text-shadow: 0 0 5px #fafafa

    @media (max-width: $mobile)
      font-size: $fs-3

  //- Description
  p
    text-align: center

//- Subscribe
newspaper-detail--subscribe
  position: absolute
  right: 0
  top: 0

  display: block
  padding: $baseline / 4

  backdrop-filter: blur(10px)

  text-align: center

  @media (max-width: $mobile)
    position: static

  .newspaper-subscription button.to-subscribe,
  .newspaper-subscription button.is-subscribed,
  .newspaper-subscription button.is-canceled,
    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    width: 150px

    line-height: $baseline * 1.5

  > p
    color: #555

    font-family: $ff-sans
    font-size: $fs--1
    line-height: 1.42
    text-align: center


newspaper-detail--info
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

  //- Editor
  a
    color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: middle


//- Editorial Intro
newspaper-detail--description
  display: grid
  grid-template-columns: 1fr 2fr
  grid-column-gap: $baseline
  grid-template-rows: auto
  margin-top: $baseline

  font-family: $ff-serif

  @media (max-width: $mobile)
    grid-template-columns: 1fr
    grid-row-gap: $baseline / 2
    padding: $baseline / 4
    margin-top: 0

  h3
    font-weight: 600

  p
    text-indent: $baseline

  footer
    margin-top: $baseline / 2

    font-weight: 600
    text-align: right

    a
      color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: middle

  picture
    height: 100%

    img
      height: 100%
      min-height: 250px
      max-height: 100%
      width: 100%
      object-fit: cover

    .image-placeholder
      min-height: 250px
      height: 100%
      background-image: radial-gradient(#fafafa, #aaa)


newspaper-detail--last-newspaper
  display: block

  timeline-newspaper
    margin-top: $baseline

newspaper-detail--empty-newspaper
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
