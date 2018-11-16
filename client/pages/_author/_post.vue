<template>
  <app-layout>
    <post-detail role="article">
      <post-detail--back-button
        title="Back"
        v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
        v-on:click="$router.go(-1)">
      </post-detail--back-button>

      <main>
        <post-detail--header>
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
            <img :src="post.author.picture" :alt="post.author.name"/>
            {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
          </nuxt-link>

          <a v-if="post.source" :href="post.source" class="external-link"><span>Original article</span></a>
        </post-detail--header>

        <post-detail--title id="start">
          <h1>{{post.content.title}}</h1>
        </post-detail--title>

        <post-detail--content v-html="post.content.perex" />

        <post-detail--continue-reading id="continue" v-if="post.content.content && showContinueReading">
          continue reading
        </post-detail--continue-reading>

        <div v-if="post.content.protected">
          <post-detail--footer>
            Rest of the article is protected. Read the orginal article here.
            <span v-if="post.source">
              Read <a :href="post.source" class="external-link">Original article</a>
            </span>
          </post-detail--footer>
        </div>

        <div v-else>
          <post-detail--content v-html="post.content.content" />

          <post-detail--footer>
            <consider-post :post="post" :showText="true" />

            <a
              :href="`https://www.facebook.com/sharer/sharer.php?u=https://kairly.com/${post.author.id}/${post.slug}`"
              target="_blank"
              class="share-fb"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              title="Share on Facebook">
            </a>

            <a
              :href="`https://twitter.com/intent/tweet?url=https://kairly.com/${post.author.id}/${post.slug}&text=${post.content.title}`"
              target="_blank"
              class="share-twitter"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              title="Share on Twitter">
            </a>
          </post-detail--footer>
        </div>

        <post-detail--author>
          <picture>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
              <img :src="post.author.picture" :alt="post.author.name"/>
            </nuxt-link>
          </picture>

          <h3>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
              {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
            </nuxt-link>
          </h3>

          <p>{{post.author.bio}}</p>

          <post-detail--author--subscription v-if="loggedIn">
            <AuthorSubscription
              v-if="subscription"
              :subscription="subscription" :author="post.author"
            />

            <button
              v-else
              @click="$refs.followWidget.openSubscribeWidget()">
              Subscribe author
            </button>

            <follow-author
              ref="followWidget"
              :author="post.author"
              :subscription="subscription"
            />
          </post-detail--author--subscription>
        </post-detail--author>
      </main>
    </post-detail>
  </app-layout>
</template>

<script>
import { errorToParams } from '@/utils/errors'
import { mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import ConsiderPost from '@/components/widgets/ConsiderPost'
import AuthorSubscription from '@/components/widgets/AuthorSubscription'
import FollowAuthor from '@/components/widgets/FollowAuthor'

export default {
  name: 'PostDetailPage', // can't use PostDetail because post-detail is already used

  auth: false,

  head() {
    var description = this.post.content.perex.replace(/<\/?[^>]+(>|$)/g, " ").substring(0,350)
    var re = /<img[^>]*src="([^"]*)"/g
    var image = null
    if (this.post.content.perex.match(re))
      image = re.exec(this.post.content.perex)[1]

    return {
      title: `${this.post.content.title} – ${this.post.author.name} – Kairly`,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: description
        },
        {
          hid: `og:title`,
          property: 'og:title',
          content: `${this.post.content.title} – ${this.post.author.name} – Kairly`
        },
        {
          hid: `og:description`,
          property: 'og:description',
          content: description
        },
        {
          hid: `og:image`,
          property: 'og:image',
          content: image
        },
        {
          hid: `og:image:alt`,
          property: 'og:image:alt',
          content: this.post.content.title
        },
        {
          hid: `og:type`,
          property: 'og:type',
          content: 'article'
        },
        {
          hid: `og:url`,
          property: 'og:url',
          content: `https://www.kairly.com/${this.post.id}`
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
          content: `${this.post.content.title} – ${this.post.author.name} – Kairly`
        },
        {
          hid: `twitter:description`,
          property: 'twitter:description',
          content: description
        },
        {
          hid: `twitter:image`,
          property: 'twitter:image',
          content: image
        },
      ]
    }
  },

  components: {
    AppLayout,
    ConsiderPost,
    FollowAuthor,
    AuthorSubscription
  },

  data() {
    return {
      showContinueReading: false
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    subscription() {
      return this.$store.getters.getAuthorSubscription(this.post.author)
    }
  },

  async asyncData({ app, store, params, error }) {
    const { author, post: postSlug } = params
    try {
      if (store.state.auth.loggedIn) {
        await store.dispatch('getSubscriptions')
      }

      const { post } = await app.$axios.$get(`/posts/${author}/${postSlug}`)
      return { post }
    } catch (err) {
      error(errorToParams(err))
    }
  },

  async created() {
    if(this.$route.hash == '#continue') {
      this.showContinueReading = true
    }

    if (process.client && this.loggedIn) {
      await this.$store.dispatch('getUserBacklog')
    }
  },

  updated() {
    // TODO dangerous if more component properties exists and updated called more
    // then once
    if (process.client && this.$route.hash) {
      const anchor = document.querySelector(this.$route.hash)
      if (anchor) {
        anchor.scrollIntoView(true)
      }
    }
  }
}
</script>

<style lang="sass">
//- POST DETAIL -//

post-detail
  position: relative

  display: block
  padding: $baseline $baseline/2 $baseline*10 $baseline/2
  min-height: calc(100vh - (#{$baseline} * 2))

  background: #fff

  @media (max-width: $mobile)
    padding: $baseline/4 $baseline/2 $baseline *5 $baseline/2

  main
    margin: 0 auto
    max-width: 700px


//- Back Button
post-detail--back-button
  position: sticky
  left: $baseline
  top: $baseline

  display: inline-block
  border-radius: 100%
  height: $baseline * 2
  width: $baseline * 2

  background: #eee

  cursor: pointer
  font-size: $fs-1
  line-height: $baseline * 2
  text-align: center

  @media (max-width: $mobile)
    display: none

  &:focus,
  &:hover
    background: $c-base
    color: #fff

  &::before
    +fa-icon()

    content: $fa-var-arrow-left

  @media (max-width: $mobile)
    position: static


//- Header
post-detail--header
  display: flex
  margin-bottom: $baseline / 2
  margin-top: -$baseline * 2
  width: 100%

  @media (max-width: $mobile)
    margin-top: 0
    margin-bottom: $baseline / 4

  a
    display: inline-block

    color: #555

    line-height: $baseline * 1.25

    //- author picture
    img
      border-radius: 100%
      float: left
      height: $baseline * 1.25
      margin-right: $baseline / 4
      width: $baseline * 1.25

      object-fit: cover

  a.external-link
    border-radius: 5px
    height: $baseline * 1.25
    margin-bottom: $baseline / 4
    margin-left: auto
    padding: 0 $baseline/4

    background: #eee
    color: #000

    cursor: pointer
    font-size: $fs--1
    line-height: $baseline * 1.25
    vertical-align: middle

    &::before
      +fa-icon()

      position: relative
      top: -1px

      margin-right: $baseline / 4

      font-size: $fs-1
      vertical-align: middle

      content: $fa-var-external-link-square

      @media (max-width: $mobile)
        margin-right: 0

        padding: 0 $baseline/4

    &:focus,
    &:hover
      background: #bbb
      color: #000

    span
      @media (max-width: $mobile)
        display: none


//- Title
post-detail--title
  display: block
  margin-bottom: $baseline / 2

  font-family: $ff-serif
  font-size: $fs-3
  font-weight: 600
  line-height: 1.7

  @media (max-width: $mobile)
    font-size: $fs-2
    line-height: 1.58


//- Continue Reading
post-detail--continue-reading
  position: relative

  display: block
  margin: $baseline*1.5 0

  margin-top: (-$baseline)   * 2
  padding-top: $baseline * 2

  color: #999

  font-family: $ff-serif
  font-size: $fs-1
  font-weight: 600
  text-align: center

  &::after,
  &::before
    position: absolute
    top: $baseline*2.5

    height: 1px
    width: 30%

    background: #eee

    content: ''

  &::before
    left: 0

  &::after
    right: 0


//- Content
post-detail--content,
post-detail--perex
  display: block

  font-family: $ff-serif
  font-size: $fs-1
  line-height: 1.7

  @media (max-width: $mobile)
    font-size: $fs-0
    line-height: 1.58

  //- title
  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  +article-content

//- Post Footer
post-detail--footer
  display: block
  padding-bottom: $baseline / 4
  margin-bottom: $baseline / 2
  margin-top: $baseline

  border-bottom: 1px solid #eee

  button-icon,
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

      margin-right: 0

      font-size: $fs-1

      content: $fa-var-facebook-square

    &.share-twitter::before
      +fa-icon()

      margin-right: 0

      font-size: $fs-1

      content: $fa-var-twitter

  //- Tweaks adding to backlog widget
  backlog-add--dropdown
    @media (max-width: 1120px)
      left: 0
      right: inherit

      margin-left: auto

      &::after
        left: $baseline
        right: inherit


//- Post Author
post-detail--author
  display: grid
  grid-template-areas: "post-detail-author-image post-detail-author-name post-detail-author-subscription" "post-detail-author-image post-detail-author-bio post-detail-author-bio"
  grid-template-columns: $baseline*3 1fr auto
  grid-template-rows: $baseline auto
  grid-gap: $baseline/4 $baseline/2

  @media (max-width: $mobile)
    grid-template-areas: "post-detail-author-image post-detail-author-name" "post-detail-author-image post-detail-author-subscription" "post-detail-author-image post-detail-author-bio"
    grid-template-columns: $baseline*3 1fr
    grid-template-rows: auto auto


  //- picture
  picture
    grid-area: post-detail-author-image

    img
      border-radius: 100%
      height: $baseline * 3
      width: $baseline * 3

      object-fit: cover

  //- name
  h3
    grid-area: post-detail-author-name

    font-size: $fs-2
    font-weight: 600

    a
      color: #000

  //- bio
  p
    grid-area: post-detail-author-bio

    line-height: 1.58

//- Author subscription
post-detail--author--subscription
  position: relative

  > button
    +subscribe-button

    height: $baseline
    padding: 0 $baseline/2

    font-family: $ff-sans
    font-size: $fs--1
    line-height: $baseline

  @media (max-width: $mobile)
    .follow-author
      left: $baseline * 2

</style>
