<template>
  <app-layout>
    <author-detail-view
      v-infinite-scroll="loadMore"
      infinite-scroll-disabled="loadingPosts"
      infinite-scroll-distance="100"
    >
      <loading-spinner v-if="loadingProfile"></loading-spinner>

      <div v-else>
        <author-detail--header>
          <picture>
            <img :src="author.picture" :alt="author.name"/>
          </picture>

          <section>
            <h1>{{ author.name }}</h1>
            <p>{{ author.bio }}</p>
          </section>

          <author-detail--subscribe>
            <button
              v-if="subscription"
              class="is-subscribed"
              @click="unfollow($event)">
              <span class="default">Subscribed</span>
              <span class="on-hover">Unsubscribe</span>
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
              :onSelect="follow" />

            <AuthorSubscription if="subscription"
              :author="author" :subscription="subscription"
            />
          </author-detail--subscribe>

        </author-detail--header>

        <author-detail--topics v-if="topics">
          <ul>
            <li v-for="topic in topics" :key="topic.url">
              <router-link :to="topic.url">{{ topic.name}}</router-link>
            </li>
          </ul>
        </author-detail--topics>

        <author-detail--newspapers v-if="newspapers.length">
          <h2>{{ author.name }}'s newspapers</h2>

          <div :class="{'show-all': showAllNewspapers}">
            <NewspaperWidget
              v-for="newspaper in newspapers"
              :key="newspaper.fullName"
              v-bind:newspaper="newspaper"
            />
          </div>

          <button v-if="newspaperIds.length > 3" v-on:click="toggleNewspapers()">{{ !showAllNewspapers ? 'Show all newspapers' : 'Hide newspapers' }}</button>

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

        <loading-spinner v-if="loadingPosts"></loading-spinner>
      </div>

    </author-detail-view>
  </app-layout>
</template>


<script>
import { mapMutations, mapGetters } from 'vuex'

import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import PostWrapper from '@/components/PostWrapper'
import FollowAuthor from '@/components/widgets/FollowAuthor'
import AuthorSubscription from '@/components/widgets/AuthorSubscription'

export default {
  name: 'AuthorDetail',

  metaInfo() {
      return {
        title: this.author ? this.author.name : undefined
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
      loadingProfile: true,
      loadingPosts: true,
      author: null,
      topic: null,
      showAllNewspapers: false,
      newspaperIds: [],
      posts: [],
      cursor: null
    }
  },

  computed: {
    newspapers() {
      const ids = this.showAllNewspapers ? this.newspaperIds : this.newspaperIds.slice(0, 3)
      return ids.map(id => this.$store.getters.newspaper(id))
    },

    subscription() {
      return this.$store.state.subscriptions.authors[this.author.id]
    },

    ...mapGetters(['user'])
  },

  watch: {
    '$route' (to, from) {
      this.loadData()
    }
  },

  methods: {
    follow(periodicity) {
      this.$store.dispatch('subscribeAuthor', {
        authorId: this.author.id,
        periodicity
      })
      ev.target.blur()
    },

    unfollow(ev) {
      this.$store.dispatch('unsubscribeAuthor', {
        authorId: this.author.id,
      })
      ev.target.blur()
    },

    toggleNewspapers() {
      this.showAllNewspapers = !this.showAllNewspapers
    },

    handlePostsData(resp) {
      resp.posts.forEach(post => this.posts.push(post))
      this.cursor = resp.cursor
      this.loadingPosts = false
    },

    loadMore() {
      if (this.cursor) {
        const { author } = this.$route.params

        this.loadingPosts = true
        api.getAuthorPosts(author, this.cursor).then(this.handlePostsData)
      }
    },

    loadData() {
      const { author } = this.$route.params

      this.loadingProfile = true
      this.loadingPosts = true
      this.author = null
      this.showAllNewspapers = false
      this.newspaperIds = []
      this.posts = []
      this.cursor = null

      api.getAuthorDetail(author).then(resp => {
        resp.newspapers.forEach(e => this.$store.dispatch('newspaperUpdated', e))
        this.author = resp.author
        this.newspaperIds = resp.newspapers.map(e => e.fullName)
        this.loadingProfile = false
        this.topics = resp.topics
      }).catch(err => {
        if (err.status == 404) {
          this.show404()
        } else {
          return Promise.reject(err)
        }
      })
      api.getAuthorPosts(author, null).then(this.handlePostsData)
    },

    ...mapMutations(['show404'])
  },

  created() {
    this.loadData()
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
  padding: $baseline/4 $baseline
  margin: 0 (-$baseline) $baseline/2 (-$baseline)

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

  text-align: center

  @media (max-width: $mobile)
    grid-column: 1 / span 2
    margin-bottom: 0

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

  h2
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

</style>
