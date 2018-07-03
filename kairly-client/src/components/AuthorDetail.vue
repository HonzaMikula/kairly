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
            <img :src="'http://kairly.com'+ author.picture" :alt="author.name"/>
          </picture>

          <section>
            <h1>{{ author.name }}</h1>
            <p>{{ author.bio }}</p>
          </section>

          <author-detail--subscribe>
            <button
              v-if="author.subscription"
              class="is-subscribed"
              @click="unfollow($event)">
              Unsubscribe author
            </button>

            <button
              v-else
              @click="$refs.followWidget.openSubscribeWidget()">
              Subscribe author
            </button>

            <follow-author
              ref="followWidget"
              :author="author"
              :onSelect="follow" />

            <AuthorSubscription if="author.subscription"
              :author="author"
            />
          </author-detail--subscribe>

        </author-detail--header>

        <author-detail--topics>
          <ul>
            <li v-for="topic in topics" :key="topic.url">
              <router-link :to="topic.url">{{ topic.name}}</router-link>
            </li>
          </ul>
        </author-detail--topics>

        <author-detail--editions v-if="editions.length">
          <h2>{{ author.name }}'s Editions</h2>

          <div>
            <EditionWidget
              v-for="edition in editions"
              :key="edition.fullName"
              v-bind:edition="edition"
            />
          </div>

          <button v-if="editionIds.length > 3" v-on:click="toggleEditions()">{{ !showAllEditions ? 'Show all editions' : 'Hide editions' }}</button>

        </author-detail--editions>


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
import { mapGetters } from 'vuex'

import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import EditionWidget from '@/components/widgets/EditionWidget'
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
    EditionWidget,
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
      showAllEditions: false,
      editionIds: [],
      posts: [],
      cursor: null
    }
  },

  computed: {
    editions() {
      const ids = this.showAllEditions ? this.editionIds : this.editionIds.slice(0, 3)
      return ids.map(id => this.$store.getters.edition(id))
    },

    ...mapGetters(['user'])
  },

  watch: {
    '$route' (to, from) {
      this.loadData()
    }
  },

  methods: {
    follow(period, time, dow) {
      // TODO split handlers
      this.$store.dispatch('invalidateTimeline')
      api.subscribeAuthor(this.author, period, time, dow).then(author => this.author)
      this.author.subscription = { period, time, dow }
    },

    unfollow(ev) {
      // TODO split handlers
      this.$store.dispatch('invalidateTimeline')
      api.unsubscribeAuthor(this.author).then(author => this.author)
      this.author.subscription = null
      ev.target.blur()
    },

    toggleEditions() {
      this.showAllEditions = !this.showAllEditions
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
      this.showAllEditions = false
      this.editionIds = []
      this.posts = []
      this.cursor = null

      api.getAuthorDetail(author).then(resp => {
        resp.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
        this.author = resp.author
        this.editionIds = resp.editions.map(e => e.fullName)
        this.loadingProfile = false
        this.topics = resp.topics
      })
      api.getAuthorPosts(author, null).then(this.handlePostsData)
    }
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

  //- Author name
  h1
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 2

  //- Bio
  p


  picture

    img
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

  button
    +subscribe-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5

    font-size: $fs-1


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

    &:first-of-type::before
      content: ''

    a
      color: $c-base

//- Editions
author-detail--editions
  display: block
  margin-bottom: $baseline

  h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

  img
    max-width: 100%

  //- wrapper for edition items
  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2
    grid-row-gap: $baseline / 2
    margin-bottom: $baseline / 2

  //- show/hide more editions
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

</style>
