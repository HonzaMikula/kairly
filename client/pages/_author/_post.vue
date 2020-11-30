<template>
  <AppLayout :name="$t('Article')">
    <div class="post-detail-view" role="article">
      <div
        v-b-tooltip
        class="post-detail--back-button"
        :title="$t('Back')"
        @click="$router.go(-1)"
      />

      <div class="post-detail--background" />

      <main itemscope itemtype="https://schema.org/NewsArticle">
        <header class="post-detail--header">
          <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
            <AuthorPicture :author="post.author" />
            {{ post.author.name }}<span v-if="post.author.medium">, {{ post.author.medium }}</span>
          </nuxt-link>

          <a v-if="post.source" :href="post.source" class="external-link" :aria-label="$t('Original article')" />
        </header>

        <div id="start" class="post-detail--title">
          <h1 itemprop="name headline mainEntityOfPage">{{ post.content.title }}</h1>
        </div>

        <div class="post-detail--content" itemprop="articleBody" v-html="post.content.perex" />

        <no-ssr>
          <div
            v-if="post.content.content && showContinueReading"
            id="continue"
            class="post-detail--continue-reading"
          >
            {{ $t('continue reading') }}
          </div>
        </no-ssr>

        <div v-if="post.content.protected && post.source && (!loggedIn || !post.content.content)">
          <footer class="post-detail--footer">
            <a :href="post.source" class="read-full-article">{{ $t('Read full article') }}</a>
          </footer>
        </div>

        <div v-else>
          <div
            class="post-detail--content"
            itemprop="articleBody"
            v-html="post.content.content"
          />

          <div class="post-detail--footer">
            <recommend-button-post
              v-if="loggedIn"
              :post="post"
              :recommended.sync="recommended"
            />

            <span
              v-if="userNewspapers.length"
              @click.stop
            >
              <button
                role="button"
                tabindex="0"
                class="consider-post"
                :class="{'is-active': isConsidered}"
                :aria-label="$t('Consider for newspaper')"
                @click.stop.prevent="openConsiderPost()"
              />

              <ConsiderPost :active.sync="showConsiderPost" :post="post" />
            </span>

            <time :title="post.time" :datetime="post.time" itemprop="datePublished dateModified">
              {{ post.time | moment('DD. MM. YYYY') }}
            </time>
          </div>
        </div>

        <div
          class="post-detail--author"
          itemprop="author"
          itemscope
          itemtype="https://schema.org/Person"
        >
          <picture>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
              <AuthorPicture itemprop="image" :author="post.author" />
            </nuxt-link>
          </picture>

          <h3>
            <nuxt-link :to="{name: 'author', params: {author: post.author.id}}" rel="author">
              <span itemprop="name">{{ post.author.name }}</span><span v-if="post.author.medium">, {{ post.author.medium }}</span>
            </nuxt-link>
          </h3>

          <p itemprop="description">{{ post.author.bio }}</p>

          <div v-if="loggedIn" class="post-detail--author--subscription">
            <AuthorSubscriptionButton :author="post.author" />
          </div>
        </div>

        <section
          v-if="editorials.length"
          class="post-detail--editorial-comments"
        >
          <h2>{{ $t('Comments by editors') }}</h2>

          <template v-for="(editorial, index) in editorials">
            <div
              v-if="editorial.type == 'article'"
              :key="'article-' + index"
              class="post-detail--editorial-comments--post"
            >
              <h3>{{ editorial.title }}</h3>
              <aside>
                {{ $t('Originally published in') }}
                <nuxt-link
                  :id="`post-editorial-newspaper-${index}`"
                  :to="{name: 'author-newspaper-issue', params: {author: editorial.issue.newspaper.editor.id, newspaper: editorial.issue.newspaper.name, issue: editorial.issue.number}}"
                >
                  {{ editorial.issue.newspaper.title }} ({{ editorial.issue.time | moment('DD. MM. YYYY') }})
                </nuxt-link>
              </aside>

              <div v-html="editorial.content" />

              <footer>
                <nuxt-link :to="{name: 'author', params: {author: editorial.author.id}}" rel="author">
                  <AuthorPicture :author="editorial.author" />
                  {{ editorial.author.name }}
                </nuxt-link>
              </footer>
            </div>
            <div
              v-if="editorial.type == 'tweets'"
              :key="'tweets-' + index"
              class="post-detail--editorial-comments--tweets"
            >
              <aside>
                {{ $t('Originally published in') }}
                <nuxt-link
                  :id="`post-editorial-newspaper-${index}`"
                  :to="{name: 'author-newspaper-issue', params: {author: editorial.issue.newspaper.editor.id, newspaper: editorial.issue.newspaper.name, issue: editorial.issue.number}}"
                >
                  {{ editorial.issue.newspaper.title }} ({{ editorial.issue.time | moment('DD. MM. YYYY') }})
                </nuxt-link>
              </aside>
              <PostTweet
                v-for="tweet in editorial.tweets"
                :key="tweet.id"
                :post="tweet"
              />
            </div>
            <NewspaperPopup
              :key="'newspaper-popup-' + index"
              :target="`post-editorial-newspaper-${index}`"
              :newspaper="editorial.issue.newspaper"
            />
          </template>
        </section>
      </main>
    </div>

    <KairlyPromo v-if="!loggedIn" />

    <FooterLinks v-if="!loggedIn" />
  </AppLayout>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import { errorToParams } from '@/utils/errors'

import AppLayout from '@/components/layout/AppLayout'
import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorSubscriptionButton from '@/components/widgets/AuthorSubscriptionButton'
import ConsiderPost from '@/components/widgets/ConsiderPost'
import FooterLinks from '@/components/microsite/FooterLinks'
import KairlyPromo from '@/components/KairlyPromo'
import NewspaperPopup from '@/components/widgets/NewspaperPopup'
import PostTweet from '@/components/posts/PostTweet'
import RecommendButtonPost from '@/components/widgets/RecommendButtonPost'

const IMG_REGEXP = /<img[^>]*src="([^"]*)"/g
const ELEMENTS_REGEXP = /<\/?[^>]+(>|$)/g

export default {
  name: 'PostDetailPage', // can't use PostDetail because post-detail is already used

  auth: false,

  components: {
    AppLayout,
    AuthorPicture,
    AuthorSubscriptionButton,
    ConsiderPost,
    FooterLinks,
    NewspaperPopup,
    KairlyPromo,
    PostTweet,
    RecommendButtonPost,
  },

  async asyncData ({ store, params, error }) {
    const { author, post: postSlug } = params
    try {
      if (store.state.auth.loggedIn) {
        await store.dispatch('getSubscriptions')
      }

      // { post, eitorials, recommended }
      return await store.dispatch('getPost', `${author}/${postSlug}`)
    } catch (err) {
      error(errorToParams(err))
    }
  },

  data () {
    return {
      showContinueReading: false,
      showConsiderPost: false,
      scrollCounter: 0
    }
  },

  head () {
    const { title, perex } = this.post.content
    const { author, id, time } = this.post
    const description = perex ? perex.replace(ELEMENTS_REGEXP, ' ').substring(0, 350) : ''

    const meta = [
      { hid: 'description', name: 'description', content: description },
      { hid: 'og:title', property: 'og:title', content: `${title} – ${author.name} – Kairly` },
      { hid: 'og:description', property: 'og:description', content: description },
      { hid: 'og:article:published_time', property: 'og:article:published_time', content: time },

      { hid: 'og:type', property: 'og:type', content: 'article' },
      { hid: 'og:url', property: 'og:url', content: `https://www.kairly.com/${id}` },
      { hid: 'twitter:card', property: 'twitter:card', content: 'summary' },
      { hid: 'twitter:site', property: 'twitter:site', content: '@kairlynews' },
      { hid: 'twitter:title', property: 'twitter:title', content: `${title} – ${author.name} – Kairly` },
      { hid: 'twitter:description', property: 'twitter:description', content: description },
      { hid: 'author', name: 'author', content: author.name },
    ]

    const matches = IMG_REGEXP.exec(perex)
    if (matches) {
      const image = matches[1]
      meta.push({ hid: 'og:image', property: 'og:image', content: image })
      meta.push({ hid: 'og:image:alt', property: 'og:image:alt', content: title })
      meta.push({ hid: 'twitter:image', property: 'twitter:image', content: image })
    }

    return {
      title: `${title} – ${author.name} – Kairly`,
      meta
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
      backlog: state => state.backlog.userBacklog
    }),

    ...mapGetters({
      userNewspapers: 'userNewspapers',
    }),

    isConsidered () {
      const backlog = this.backlog ? (this.backlog[this.post.id] || {}) : {}

      return Object.keys(backlog).length > 0
    }
  },

  created () {
    if (this.$route.hash === '#continue') {
      this.showContinueReading = true
    }
  },

  async mounted () {
    if (this.loggedIn) {
      await this.$store.dispatch('backlog/loadUserBacklog')
    }
  },

  updated () {
    // TODO dangerous if more component properties exists and updated called more
    // then once
    if (this.$route.hash && this.scrollCounter === 0) {
      const anchor = document.querySelector(this.$route.hash)
      if (anchor) {
        anchor.scrollIntoView(true)
        this.scrollCounter++
      }
    }
  },

  methods: {
    closeConsiderPost () {
      this.showConsiderPost = false
    },

    openConsiderPost () {
      this.showConsiderPost = true
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'
@import './styles/components/article-content'

//- POST DETAIL -//
.post-detail-view
  position: relative

  display: block
  padding: $baseline $baseline/2 $baseline $baseline/2
  min-height: calc(100vh - (#{$baseline} * 2))

  .post-detail--background
    position: absolute
    top: 0
    left: 0

    height: 100%
    width: 100%

    background: #fafafa url('~assets/article/paper-noise.jpg') fixed
    background-size: cover
    filter: blur(10px) brightness(108%)

  @media (max-width: $mobile)
    padding: $mBaseline/2 $mBaseline $mBaseline $mBaseline

  main
    position: relative
    z-index: 1

    margin: 0 auto
    padding: $baseline
    max-width: 700px

    background: #fff

//- Back Button
.post-detail--back-button
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
.post-detail--header
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
.post-detail--title
  display: block
  margin-bottom: $baseline / 2

  font-family: $ff-serif
  font-size: $fs-3
  font-weight: 600
  line-height: 1.8

  @media (max-width: $mobile)
    font-size: $fs-2
    line-height: 1.58

//- Continue Reading
.post-detail--continue-reading
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
.post-detail--content,
.post-detail--perex
  display: block

  font-family: $ff-serif
  font-size: $fs-1
  line-height: 1.8

  //- title
  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  +article-content

//- Post Footer
.post-detail--footer
  display: flex
  align-items: center
  padding-bottom: $baseline / 2
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

    &.is-active
      background: lighten($c-base, 20%)

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
.post-detail--author
  display: grid
  grid-template-areas: "post-detail-author-image post-detail-author-name post-detail-author-subscription" "post-detail-author-image post-detail-author-bio post-detail-author-bio"
  grid-template-columns: $baseline*3 1fr auto
  grid-template-rows: $baseline auto
  grid-gap: $baseline/4 $baseline/2
  margin-bottom: $baseline
  padding-bottom: $baseline / 2

  border-bottom: 1px solid #eee

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
.post-detail--author--subscription
  position: relative

  .author-subscription-view
    //- when newspaper is subscribed
    button.is-subscribed
      +button(primary, small)

    //- when newspeper is suspended
    button.is-suspended
      +button(secondary, small)

      background: lighten($c-base, 10%)
      background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)

    //- when newspaper is ready to be subsribed
    //- when newspeper is canceled
    button.to-subscribe,
    button.is-canceled
      +button(secondary, small)

//- Editorial Comments
.post-detail--editorial-comments

  > h2
    margin-bottom: $baseline / 2

    font-weight: 600
    font-size: $fs-2

//- Editorial post
.post-detail--editorial-comments--post
  padding: $baseline / 2
  margin-bottom: $baseline / 2

  background: #F2ECEC

  font-family: $ff-serif

  @media (max-width: $mobile)
    margin-left: (-$mBaseline)
    margin-right: (-$mBaseline)

  > h3
    font-weight: 600
    font-size: $fs-1

  //- originally published ...
  aside
    margin-bottom: $baseline / 2

    font-size: $fs--1
    font-family: $ff-sans
    line-height: 1.42

    a
      color: $c-base

  //- content
  aside + div
    p
      margin-bottom: $baseline

      &:last-of-type //- TODO: P doesn't have to be the last item
        margin-bottom: $baseline / 2

    h2, h3, h4, h5, h6
      margin-bottom: $baseline / 4
      font-weight: 600

  footer
    a
      display: flex
      align-items: center

      font-family: $ff-sans
      font-weight: 600

      color: #000

      img
        border-radius: 100%
        height: $baseline
        margin-right: $baseline / 4
        width: $baseline

//- Editorial post
.post-detail--editorial-comments--tweets
  padding: $baseline / 2
  margin-bottom: $baseline / 2

  background: #F2ECEC

  font-family: $ff-serif

  @media (max-width: $mobile)
    margin: 0 (-$mBaseline)

  aside
    margin-bottom: $baseline / 2

    font-size: $fs--1
    font-family: $ff-sans
    line-height: 1.42

    a
      color: $c-base

  > article.post.tweet
    margin-bottom: $baseline
    max-width: none
    padding: 0

    background: transparent

    &:last-of-type
      margin-bottom: 0

    .timeline-post--tweet
      font-size: $fs-0
</style>
