<template>
  <app-layout>
    <issue-detail-view>
      <Issue :issue="issue" :subscription="newspaper.subscription" />
    </issue-detail-view>

    <div class="issue--footer">
      <h2>{{ newspaper.title }}</h2>

      <picture>
        <img :src="newspaper.picture" :alt="newspaper.title" />
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

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'

export default {
  name: 'IssueDetail',

  auth: false,

  head() {
      return {
        title: `${this.newspaper.title} #${this.issue.number} – Kairly`,
        meta: [
          {
            hid: 'description',
            name: 'description',
            content: this.newspaper.description
          },
          {
            hid: `og:title`,
            property: 'og:title',
            content: `${this.newspaper.title} #${this.issue.number} – Kairly`
          },
          {
            hid: `og:description`,
            property: 'og:description',
            content: this.newspaper.description
          },
          {
            hid: `og:image`,
            property: 'og:image',
            content: this.newspaper.picture
          },
          {
            hid: `og:image:alt`,
            property: 'og:image:alt',
            content: this.newspaper.title
          },
          {
            hid: `og:type`,
            property: 'og:type',
            content: 'product'
          },
          {
            hid: `og:url`,
            property: 'og:url',
            content: `https://www.kairly.com/${this.newspaper.editor.id}/${this.newspaper.name}/${this.issue.number}`
          },
          {
            hid: `twitter:card`,
            property: 'twitter:card',
            content: 'summary'
          },
          {
            hid: `twitter:site`,
            property: 'twitter:site',
            content: '@kairlyapp'
          },
          {
            hid: `twitter:title`,
            property: 'twitter:title',
            content: `${this.newspaper.title} #${this.issue.number} – Kairly`
          },
          {
            hid: `twitter:description`,
            property: 'twitter:description',
            content: this.newspaper.description
          },
          {
            hid: `twitter:image`,
            property: 'twitter:image',
            content: this.newspaper.picture
          },
        ]
      }
  },

  components: {
    AppLayout,
    Issue,
    NewspaperSubscription
  },

  data() {
    return {
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    periodicity() {
      if (this.newspaper.periodicity.frequency == '3x_per_day') {
        return 'Daily at 6:00, 12:00 and 18:00'
      }
      else if (this.newspaper.periodicity.frequency == 'daily') {
        return `Daily at ${this.newspaper.periodicity.time}`
      }
      else {
        return `Every ${this.DAYS[this.newspaper.periodicity.dow -1]} at ${this.newspaper.periodicity.time}`
      }
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
        issues: [params.issue]
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
  grid-template-areas: "issue-footer-picture issue-footer-title issue-footer-subscription" "issue-footer-picture issue-footer-description issue-footer-subscription"
  grid-template-columns: $baseline*7 1fr auto
  grid-template-rows: $baseline auto
  grid-gap: $baseline/4 $baseline/2

  margin: $baseline*2 auto 0 auto
  max-width: 900px
  padding: $baseline/2 0 $baseline 0

  border-top: 1px solid #eee

  //- picture
  picture
    grid-area: issue-footer-picture

    img
      width: 100%


  //- title
  h2
    grid-area: issue-footer-title

    font-weight: 600
    font-size: $fs-2

  //- description
  .issue--footer--description
    grid-area: issue-footer-description

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
