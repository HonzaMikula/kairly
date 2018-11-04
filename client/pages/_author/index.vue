<template>
  <app-layout>
    <author-detail-view
      v-infinite-scroll="loadPosts"
      infinite-scroll-disabled="loadingPosts"
      infinite-scroll-distance="100"
    >
      <author-detail--header>
        <picture>
          <img v-if="author.picture" :src="author.picture" :alt="author.name" />
          <img v-else src="~assets/user.png" :alt="author.name"/>
        </picture>

        <section>
          <h1>{{ author.name }}</h1>
          <p>{{ author.bio }}</p>
        </section>

        <author-detail--subscribe v-if="loggedIn">
          <button
            v-if="subscription"
            :class="{'is-subscribed': subscription.renewal, 'is-canceled': !subscription.renewal}"
            @click="subscription.renewal ? unsubscribe() : renewSubscription()">
            <span class="default">
              <template v-if="subscription.renewal">Subscribed</template>
              <template v-else>Canceled</template>
            </span>
            <span class="on-hover" v-if="subscription.renewal">Unsubscribe</span>
            <span
              v-else
              class="on-hover"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="`Subscribtion last till ${subscription.to}`">
              Renew
            </span>
          </button>

          <button
            class="to-subscribe"
            v-else
            @click="$refs.followWidget.openSubscribeWidget()">
            Subscribe
          </button>

          <follow-author
            ref="followWidget"
            :author="author"
            :subscription="subscription"
          />

          <AuthorSubscription if="subscription"
            :author="author" :subscription="subscription"
          />
        </author-detail--subscribe>

      </author-detail--header>

      <author-detail--topics v-if="topics">
        <ul>
          <li v-for="topic in topics" :key="topic.url">
            <nuxt-link :to="topic.url">{{ topic.name}}</nuxt-link>
          </li>
        </ul>
      </author-detail--topics>

      <author-detail--newspapers v-if="newspapers.length">
        <h2>{{ author.name }}'s newspapers</h2>

        <div :class="{'show-all': showAllNewspapers}">
          <NewspaperWidget
            v-for="newspaper in visibleNewspapers"
            :key="newspaper.fullName"
            v-bind:newspaper="newspaper"
          />
        </div>

        <button v-if="newspapers.length > 3" v-on:click="toggleNewspapers()">{{ !showAllNewspapers ? 'Show all newspapers' : 'Hide newspapers' }}</button>

      </author-detail--newspapers>


      <author-detail--posts v-if="posts.length">
        <h2>{{ author.name }}'s Posts</h2>

        <PostWrapper
          v-for="post in posts"
          :post="post"
          :isSubscribed="true"
          :key="post.id"
        />
      </author-detail--posts>

      <div class="author-detail--empty" v-if="!newspapers.length && !posts.length && !loadingPosts">
        <template v-if="test.user.id !== author.id">
          <p>User didn't write any posts and didn't start any newspaper.</p>
        </template>

        <template v-else>
          <p>You didn't write any post and didn't start any newspaper.</p>

          <nuxt-link :to="{name: 'newspapers'}">Start a newspaper</nuxt-link>
        </template>

      </div>

      <loading-spinner v-if="loadingPosts"></loading-spinner>

    </author-detail-view>
  </app-layout>
</template>


<script>
import { mapMutations, mapState } from 'vuex'
import { errorToParams } from '@/utils/errors'

import AppLayout from '@/components/layout/AppLayout'
import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import PostWrapper from '@/components/PostWrapper'
import FollowAuthor from '@/components/widgets/FollowAuthor'
import AuthorSubscription from '@/components/widgets/AuthorSubscription'

export default {
  name: 'AuthorDetail',

  auth: false,

  head() {
    return {
      title: this.author ? this.author.name + ' – Kairly' : undefined,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.author.bio
        },
        {
          hid: `og:title`,
          property: 'og:title',
          content: `${this.author.name} – Kairly`
        },
        {
          hid: `og:description`,
          property: 'og:description',
          content: this.author.bio
        },
        {
          hid: `og:image`,
          property: 'og:image',
          content: this.author.picture
        },
        {
          hid: `og:image:alt`,
          property: 'og:image:alt',
          content: this.author.name
        },
        {
          hid: `og:type`,
          property: 'og:type',
          content: 'profile'
        },
        {
          hid: `og:url`,
          property: 'og:url',
          content: `https://www.kairly.com/${this.author.id}`
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
          content: `${this.author.name} – Kairly`
        },
        {
          hid: `twitter:description`,
          property: 'twitter:description',
          content: this.author.bio
        },
        {
          hid: `twitter:image`,
          property: 'twitter:image',
          content: this.author.picture
        },
      ]
    }
  },

  components: {
    AppLayout,
    NewspaperWidget,
    PostWrapper,
    FollowAuthor,
    AuthorSubscription
  },

  data() {
    return {
      showAllNewspapers: false
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
      test: state => state.auth
    }),

    visibleNewspapers() {
      return this.showAllNewspapers ? this.newspapers : this.newspapers.slice(0, 3)
    },

    subscription() {
      return this.$store.getters.getAuthorSubscription(this.author)
    }
  },

  methods: {
    unsubscribe() {
      this.$store.dispatch('unsubscribeAuthor', {
        author: this.author,
      })
      document.activeElement.blur()
    },

    renewSubscription() {
      this.$store.dispatch('subscribeAuthor', {
        author: this.author
      })
      document.activeElement.blur()
    },

    toggleNewspapers() {
      this.showAllNewspapers = !this.showAllNewspapers
    },

    async loadPosts() {
      if (this.cursor === null) {
        return
      }
      const { author: authorId } = this.$route.params

      this.loadingPosts = true

      const { posts, cursor } = await this.$axios.$get(
        `/authors/${authorId}/posts`, {params: {cursor: this.cursor}})

      posts.forEach(post => this.posts.push(post))
      this.cursor = cursor
      this.loadingPosts = false
    }
  },

  async asyncData({ app, store, params: { author: authorId }, error}) {
    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }

    try {
      const { author, newspapers, topics=null } = await store.dispatch('getAuthor', authorId)

      const data = {
        author,
        newspapers,
        topics
      }

      if (process.server) {
        const { posts, cursor } = await app.$axios.$get(
          `/authors/${authorId}/posts`, {params: {cursor: 0}})
        data.posts = posts
        data.cursor = cursor
        data.loadingPosts = false
      } else {
        // load all in created function to make transition faster
        data.posts = []
        data.cursor = 0
        data.loadingPosts = true
      }

      return data
    } catch (err) {
      error(errorToParams(err))
    }
  },

  created() {
    if (process.client && this.cursor === 0) {
      this.loadPosts()
    }
  },
}
</script>

<style lang="sass">
//- AUTHOR DETAIL -//

author-detail-view
  display: block
  padding-top: $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding-top: 0


//- Header
author-detail--header
  position: sticky
  top: 0
  z-index: 1

  display: grid
  grid-template-columns: $baseline*4 1fr auto
  grid-column-gap: $baseline
  padding: $baseline/4 $baseline $baseline/4 $baseline
  margin: (-$baseline/4) (-$baseline) $baseline/2 (-$baseline)

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: $mobile)
    position: static
    grid-template-columns: $baseline*4 1fr
    grid-template-rows: auto auto
    grid-row-gap: $baseline / 2
    padding: $baseline / 4
    margin: 0

  //- Author name
  h1
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 2
    text-shadow: 0 0 5px #fafafa

  //- Bio
  p
    text-shadow: 0 0 5px #fafafa

  picture img
    display: block
    border-radius: 100%
    height: $baseline * 4
    width: $baseline * 4

    object-fit: cover


//- Subsribe
author-detail--subscribe
  position: relative

  display: block
  margin-bottom: $baseline

  color: #555

  font-family: $ff-sans
  line-height: 1.42
  text-align: center

  @media (max-width: $mobile)
    grid-column: 1 / span 2
    margin-bottom: 0

  //- when author is subscribed
  button.is-subscribed
    +subscribed-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    width: 150px

    line-height: $baseline * 1.5

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when author is canceled
  button.is-canceled
    +subscribed-button

    border-radius: $baseline * 0.5
    height: $baseline * 1.5
    width: 140px

    line-height: $baseline * 1.5

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  //- when author is ready to be subsribed
  button.to-subscribe
    +subscribe-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    width: 150px

    line-height: $baseline * 1.5


//- Topics
author-detail--topics
  display: table
  margin: 0 auto $baseline auto

  li
    display: inline-block

    &::before
      display: inline-block
      padding: 0 $baseline/2

      content: '•'

      @media (max-width: $mobile)
        padding: 0 $baseline/4

    &:first-of-type::before
      content: ''

    a
      color: $c-base

//- Newspapers
author-detail--newspapers
  display: block
  margin-bottom: $baseline

  @media (max-width: $mobile)
    padding: $baseline / 4

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

  img
    max-width: 100%

  //- wrapper for newspaper items
  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2
    grid-row-gap: $baseline / 2
    margin-bottom: $baseline / 2

    @media (max-width: $mobile)
      grid-template-columns: 1fr 1fr
      grid-column-gap: $baseline / 4

      newspaper-widget-view:last-of-type
        display: none

      &.show-all newspaper-widget-view:last-of-type
        display: block

  //- show/hide more newspapers
  > button
    display: table
    border-radius: $baseline
    height: $baseline * 1.25
    padding: 0 $baseline
    margin: 0 auto

    background: $c-base
    border: 0
    color: #fff

    font-family: $ff-sans
    font-size: $fs--1
    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)

//- Posts
author-detail--posts
  display: block
  margin-bottom: $baseline

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      padding: 0 $baseline/4

//- Empty
.author-detail--empty
  padding: $baseline
  margin-top: $baseline * 2

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  a
    +subscribed-button

    display: inline-block
    margin-top: $baseline

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
