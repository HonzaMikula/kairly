<template>
  <app-layout>
    <issue-detail-view>
      <Issue :issue="issue" :subscription="newspaper.subscription">
        <template slot="newspaperTitle">{{ newspaper.title }} #{{issue.number}}</template>
      </Issue>
    </issue-detail-view>

    <div class="issue--footer">
      <h2>
        <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">
          {{ newspaper.title }}
        </nuxt-link>
      </h2>

      <picture>
        <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">
          <img v-if="newspaper.picture" :src="newspaper.picture" :alt="newspaper.title" />
          <div v-else class="image-placeholder"></div>
        </nuxt-link>
      </picture>

      <div class="issue--footer--description">
        <ul>
          <li class="author">
            <nuxt-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
              <img :src="newspaper.editor.picture" :alt="newspaper.editor.name" />
              {{newspaper.editor.name}}
            </nuxt-link>
          </li>

          <li>#{{ newspaper.issues }}</li>

          <li>{{ newspaper.likes }} readers</li>

          <li>49 CZK / month</li>
        </ul>

        <p>{{ newspaper.description }}</p>
      </div>

      <div class="issue--footer--subscription" v-if="loggedIn">
        <newspaper-subscription :newspaper="newspaper" />

        <p>{{ periodicity }}</p>
      </div>
    </div>
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
  name: 'IssueDetail',

  auth: false,

  head() {
    const { title, name, description, editor, picture } = this.newspaper
    const { number } = this.issue
    return {
      title: `${title} #${number} – Kairly`,
      meta: [
        { hid: 'description', name: 'description', content: description },
        { hid: 'og:title', property: 'og:title', content: `${title} #${number} – Kairly` },
        { hid: 'og:description', property: 'og:description', content: description },
        { hid: 'og:image', property: 'og:image', content: picture },
        { hid: 'og:image:alt', property: 'og:image:alt', content: title },
        { hid: 'og:type', property: 'og:type', content: 'product' },
        { hid: 'og:url', property: 'og:url', content: `https://www.kairly.com/${editor.id}/${name}/${number}`},
        { hid: 'twitter:card', property: 'twitter:card', content: 'summary'},
        { hid: 'twitter:site', property: 'twitter:site', content: '@kairlyapp'},
        { hid: `twitter:title`, property: 'twitter:title', content: `${title} #${number} – Kairly` },
        { hid: `twitter:description`, property: 'twitter:description', content: description },
        { hid: `twitter:image`, property: 'twitter:image', content: picture },
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
      const { newspaper, issues } = await store.dispatch('getNewspaperDetail', {
        newspaperId: fullName,
        issue: params.issue
      })
      return { newspaper, issue: issues[0] }
    } catch (err) {
      error(errorToParams(err))
    }
  }
}
</script>

<style lang="sass">
issue-detail-view
  display: block
  margin: $baseline auto 0 auto
  max-width: 900px

.issue--footer
  display: grid
  box-sizing: border-box
  grid-template-areas: "issue-footer-picture issue-footer-title issue-footer-subscription" "issue-footer-picture issue-footer-description issue-footer-subscription"
  grid-template-columns: $baseline*7 1fr auto
  grid-template-rows: $baseline auto
  grid-gap: $baseline/4 $baseline/2
  margin: $baseline*2 auto 0 auto
  max-width: 900px
  padding: $baseline/2 $baseline/2 $baseline $baseline/2

  border-top: 1px solid #eee

  @media (max-width: $mobile)
    grid-template-areas: "issue-footer-picture issue-footer-title" "issue-footer-picture issue-footer-description" "issue-footer-picture issue-footer-subscription"
    grid-template-columns: $baseline*7 1fr
    grid-template-rows: auto auto auto
    padding: $baseline/4

  @media (max-width: 480px)
    grid-template-areas: "issue-footer-picture" "issue-footer-title" "issue-footer-description" "issue-footer-subscription"
    grid-template-columns: 1fr

  //- picture
  picture
    grid-area: issue-footer-picture

    img
      width: 100%

    .image-placeholder
      height: 100%
      background-image: radial-gradient(#fafafa, #aaa)


  //- title
  h2
    grid-area: issue-footer-title

    font-weight: 600
    font-size: $fs-2

    a
      color: #000

  //- description
  .issue--footer--description
    grid-area: issue-footer-description

    p
      line-height: 1.42

    ul
      margin-bottom: $baseline / 4

    li
      display: inline-block
      vertical-align: middle

      color: #777

      font-weight: 600

      &::after
        display: inline-block
        padding: 0 $baseline/4

        content: '•'

      &:last-of-type::after
        content: ''

      &.author img
        border-radius: 100%
        float: left
        height: $baseline
        margin-right: $baseline / 4
        width: $baseline

      a
        color: #777

        &:focus,
        &:hover
          color: #000


  //- subscription
  .issue--footer--subscription
    grid-area: issue-footer-subscription

    text-align: center

</style>
