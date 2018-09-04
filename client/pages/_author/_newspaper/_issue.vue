<template>
  <app-layout>
    <issue-detail-view>
      <Issue :issue="issue" :subscription="newspaper.subscription" />
    </issue-detail-view>
  </app-layout>
</template>


<script>
import { mapActions } from 'vuex'

import { errorToParams } from '@/utils/errors'

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'

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
    Issue
  },

  async asyncData({ store, params, error }) {
    const fullName = `${params.author}/${params.newspaper}`

    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }

    try {
      const { newspaper, issue } = await store.dispatch('getNewspaperDetail', {
        newspaperId: fullName,
        issue: params.issue
      })
      return { newspaper, issue }
    } catch (err) {
      error(errorToParams(err))
    }
  }
}
</script>

<style lang="sass">
issue-detail-view
  display: block
  margin: $baseline auto
  max-width: 900px
</style>
