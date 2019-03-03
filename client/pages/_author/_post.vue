<template>
  <app-layout :name="$t('Article')">
    <post-detail role="article">
      <post-detail--back-button
        :title="$t('Back')"
        v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
        @click="$router.go(-1)">
      </post-detail--back-button>

      <main itemscope itemtype="https://schema.org/NewsArticle">
        <post-detail--header>
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
            <img :src="post.author.picture" :alt="post.author.name"/>
            {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
          </nuxt-link>

          <a v-if="post.source" :href="post.source" class="external-link" :aria-label="$t('Original article')"></a>
        </post-detail--header>

        <post-detail--title id="start">
          <h1 itemprop="name headline">{{post.content.title}}</h1>
        </post-detail--title>

        <post-detail--content v-html="post.content.perex" itemprop="articleBody" />

        <no-ssr>
          <post-detail--continue-reading id="continue" v-if="post.content.content && showContinueReading">
            {{ $t('continue reading') }}
          </post-detail--continue-reading>
        </no-ssr>

        <div v-if="post.content.protected && post.source">
          <post-detail--footer>
            <a :href="post.source" class="read-full-article">{{ $t('Read full article') }}</a>
          </post-detail--footer>
        </div>

        <div v-else>
          <post-detail--content v-html="post.content.content" itemprop="articleBody" />

          <post-detail--footer>
            <span v-if="userNewspapers.length" @click.stop>
              <button
                role="button"
                tabindex="0"
                class="consider-post"
                @click.stop.prevent="openConsiderPost()"
                :aria-label="$t('Consider for newspaper')">
              </button>

              <consider-post v-if="showConsiderPost" :post="post" @closeConsiderPostDialog="closeConsiderPost" />
            </span>

            <a
              :href="`https://www.facebook.com/sharer/sharer.php?u=https://kairly.com/${post.author.id}/${post.slug}`"
              target="_blank"
              class="share-fb"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="$t('Share on Facebook')">
            </a>

            <a
              :href="`https://twitter.com/intent/tweet?url=https://kairly.com/${post.author.id}/${post.slug}&text=${post.content.title}`"
              target="_blank"
              class="share-twitter"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              :title="$t('Share on Twitter')">
            </a>

            <time :title="post.time" :datetime="post.time" itemprop="datePublished dateModified">
              {{ post.time | moment('DD. MM. YYYY') }}
            </time>
          </post-detail--footer>
        </div>

        <post-detail--author itemprop="author publisher" itemscope itemtype="https://schema.org/Person">
          <picture>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
              <img itemprop="image" :src="post.author.picture" :alt="post.author.name"/>
            </nuxt-link>
          </picture>

          <h3>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
              <span itemprop="name">{{post.author.name}}</span><span v-if="post.author.medium">, {{post.author.medium}}</span>
            </nuxt-link>
          </h3>

          <p itemprop="description">{{post.author.bio}}</p>

          <post-detail--author--subscription v-if="loggedIn">
            <AuthorSubscription
              v-if="subscription"
              :subscription="subscription" :author="post.author"
            />
          </post-detail--author--subscription>
        </post-detail--author>
      </main>
    </post-detail>

    <KairlyPromo v-if="!loggedIn" />

    <FooterLinks v-if="!loggedIn" />
  </app-layout>
</template>

<script>
import { errorToParams } from '@/utils/errors'
import { mapGetters, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import ConsiderPost from '@/components/widgets/ConsiderPost'
import AuthorSubscription from '@/components/widgets/AuthorSubscription'
import KairlyPromo from '@/components/KairlyPromo'
import FooterLinks from '@/components/microsite/FooterLinks'

const IMG_REGEXP = /<img[^>]*src="([^"]*)"/g
const ELEMENTS_REGEXP = /<\/?[^>]+(>|$)/g

export default {
  name: 'PostDetailPage', // can't use PostDetail because post-detail is already used

  auth: false,

  head() {
    const { title, perex }  = this.post.content
    const { author, id } = this.post
    const description = perex ? perex.replace(ELEMENTS_REGEXP, ' ').substring(0,350) : ''

    const meta = [
      { hid: 'description', name: 'description', content: description},
      { hid: `og:title`, property: 'og:title', content: `${title} – ${author.name} – Kairly`},
      { hid: `og:description`, property: 'og:description', content: description},


      { hid: `og:type`, property: 'og:type', content: 'article'},
      { hid: `og:url`, property: 'og:url', content: `https://www.kairly.com/${id}`},
      { hid: `twitter:card`, property: 'twitter:card', content: 'summary'},
      { hid: `twitter:site`, property: 'twitter:site', content: '@kairlyapp'},
      { hid: `twitter:title`, property: 'twitter:title', content: `${title} – ${author.name} – Kairly`},
      { hid: `twitter:description`, property: 'twitter:description', content: description},
    ]

    const matches =  IMG_REGEXP.exec(perex)
    if (matches) {
      const image = matches[1]
      meta.push({ hid: `og:image`, property: 'og:image', content: image})
      meta.push({ hid: `og:image:alt`, property: 'og:image:alt', content: title})
      meta.push({ hid: `twitter:image`, property: 'twitter:image', content: image})
    }

    return {
      title: `${title} – ${author.name} – Kairly`,
      meta
    }
  },

  components: {
    AppLayout,
    ConsiderPost,
    AuthorSubscription,
    KairlyPromo,
    FooterLinks
  },

  data() {
    return {
      showContinueReading: false,
      showConsiderPost: false,
      scrollCounter: 0
    }
  },

  methods: {
    closeConsiderPost() {
      this.showConsiderPost = false
    },

    openConsiderPost() {
      this.showConsiderPost = true
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    ...mapGetters(['userNewspapers']),

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
    if (process.client && this.$route.hash && this.scrollCounter == 0) {
      const anchor = document.querySelector(this.$route.hash)
      if (anchor) {
        anchor.scrollIntoView(true)
        this.scrollCounter++
      }
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'
@import './styles/components/article-content'

//- POST DETAIL -//

post-detail
  position: relative

  display: block
  padding: $baseline $baseline/2 $baseline $baseline/2
  min-height: calc(100vh - (#{$baseline} * 2))

  background: #fff

  @media (max-width: $mobile)
    padding: $mBaseline/2 $mBaseline $mBaseline *5 $mBaseline

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
    @extend .fas

    content: fa-content($fa-var-arrow-left)

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
    +button-icon($fa-var-external-link-square-alt, icon-text)

    margin-left: auto

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

    @media (max-width: $mobile)
      width: 50px

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

  //- title
  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  +article-content

//- Post Footer
post-detail--footer
  display: flex
  padding-bottom: $baseline / 4
  margin-bottom: $baseline / 2
  margin-top: $baseline

  border-bottom: 1px solid #eee

  > span,
  > a
    margin-right: $baseline / 2

  //- consider button
  > span
    position: relative

  .consider-post
    +button-icon($fa-var-newspaper, icon-text)

  //- share FB button
  .share-fb
    +button-icon($fa-var-facebook, icon, brand)

  //- share Twitter button
  .share-twitter
    +button-icon($fa-var-twitter, icon, brand)


  a.read-full-article
    +button(primary, large)

    display: table
    margin: 0 auto $baseline auto

  time
    margin-left: auto

  //- Tweaks adding to backlog widget
  .consider-post-view
    @media (max-width: 1120px)
      left: 0
      right: inherit

      margin-left: auto

      &::after
        left: $baseline * 0.75
        right: inherit


//- Post Author
post-detail--author
  display: grid
  grid-template-areas: "post-detail-author-image post-detail-author-name post-detail-author-subscription" "post-detail-author-image post-detail-author-bio post-detail-author-bio"
  grid-template-columns: $baseline*3 1fr auto
  grid-template-rows: $baseline auto
  grid-gap: $baseline/4 $baseline/2
  padding-bottom: $baseline * 5

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

  .author-subscription-view
    //- when newspaper is subscribed
    button.is-subscribed
      +button(primary, medium)

    //- when newspeper is suspended
    button.is-suspended
      +button(secondary, medium)

      background: lighten($c-base, 10%)
      background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

    //- when newspaper is ready to be subsribed
    //- when newspeper is canceled
    button.to-subscribe,
    button.is-canceled
      +button(secondary, medium)

</style>
