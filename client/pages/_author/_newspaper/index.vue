<template>
  <AppLayout :name="$t('Newspaper detail')">
    <div class="newspaper-detail" itemtype="https://schema.org/Newspaper" itemscope>
      <header class="newspaper-detail--header">
        <div>
          <h1 itemprop="name">
            <nuxt-link
              :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">
              {{ newspaper.title }}
            </nuxt-link>
          </h1>
          <p>{{ newspaper.description }}</p>

          <picture itemprop="image">
            <img
              v-if="newspaper.picture"
              :src="newspaper.picture"
              :alt="newspaper.title"
            />
            <div v-else class="image-placeholder"></div>
          </picture>

          <div
            v-if="loggedIn"
            class="newspaper-detail--subscribe"
          >
            <NewspaperSubscriptionButton :newspaper="newspaper" />

            <p>{{ periodicity }}</p>
          </div>
        </div>
      </header>

      <main>
        <template v-if="issue">
          <nav
            v-if="links.prev || links.next"
            class="newspaper-detail--navigation"
          >
            <nuxt-link
              v-if="links.prev"
              :to="links.prev"
              v-b-tooltip
              :title="$t('Previous issue')"
              class="previous"
            />

            <nuxt-link
              v-if="links.next"
              :to="links.next"
              v-b-tooltip
              :title="$t('Next issue')"
              class="next"
            />
          </nav>

          <div class="newspaper-detail--issue">
            <IssueWrapper
              :issue="issue"
              :subscription="newspaper.subscription"
              hideDate
              showTail
            >
              <template #newspaper-title>
                {{ $t('Issue from') }}
                <time itemprop="datePublished">{{ issue.time | moment('D. M. YYYY')}}</time>
              </template>
            </IssueWrapper>

            <p>{{ $t('That\'s it. You read the whole issue.') }}</p>
          </div>

          <footer 
            class="newspaper-detail--newsletter-subscription">
            <h2>{{ $t('Subscribe to newsletter') }}</h2>
            <ul>
              <li>
                {{ $t('Read the best content selected by') }}

                <nuxt-link
                  :to="{name: 'author', params: {author: newspaper.editor.id}}"
                  :id="`issue-newspaper-author-${$_uid}`"
                >
                  <img :src="newspaper.editor.pictures.small" :alt="newspaper.editor.name" />
                  <strong>{{ newspaper.editor.name }}</strong>
                </nuxt-link>.
              </li>
              <li>{{ $t('You will receive newsletter in your inbox') }} <strong class="periodicity">{{ periodicity }}</strong>.</li>
              <li>
                {{ $t('You can also subscribe using') }}
                <a
                  :href="`https://kairly.com/${newspaper.editor.id}/${newspaper.name}/rss`"
                  target="_blank"
                  class="rss"
                  :aria-label="$t('Subscribe RSS')"
                  v-b-tooltip
                  :title="$t('Subscribe RSS')"
                  @click="$ga.event({
                    eventCategory: 'Subscribe RSS newspaper',
                    eventAction: newspaper.name,
                    eventLabel: newspaper.editor.id
                  })"
                >{{ $t('RSS feed') }}</a>.
              </li>
            </ul>
            <!-- Begin Mailchimp Signup Form -->
            <div
              v-if="newspaper.newsletterSubscriptionUrl"
              id="mc_embed_signup"
            >
              <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
                <div id="mc_embed_signup_scroll">
                  <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" :placeholder="$t('email address')" required>
                  <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signupss -->
                  <div style="position: absolute; left: -5000px;" aria-hidden="true">
                    <input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value="">
                    <input type="checkbox" :value="newspaper.newsletterSubscriptionUrl" :name="`group[84705][${newspaper.newsletterSubscriptionUrl}]`" checked />
                  </div>
                  <div class="clear">
                    <input
                      id="mc-embedded-subscribe"
                      type="submit"
                      :value="$t('Subscribe')"
                      name="subscribe"
                      class="button"
                      @click="$ga.event({
                        eventCategory: 'Subscribe newspaper newsletter',
                        eventAction: newspaper.name,
                        eventLabel: newspaper.editor.id
                      })"
                    />
                  </div>
                </div>
              </form>
            </div>
            <!--End mc_embed_signup -->
              
          </footer>
        </template>

        <div
          v-else
          class="newspaper-detail--empty-newspaper"
        >
          <h2>{{ $t('No issue yet') }}</h2>
          <p>
            {{ $t('Subscribe the newspaper and once it\'s published, we will show you on your timeline.') }}
          </p>
        </div>
      </main>
    </div>
    <KairlyPromo v-if="!loggedIn" />

    <FooterLinks v-if="!loggedIn" />
  </AppLayout>
</template>

<script>
/*
  Don't forget that
  /:author/:newspaper/:issue is also routed to this page
*/

import { mapState, mapMutations, mapActions } from 'vuex'

import { errorToParams } from '@/utils/errors'

import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import AppLayout from '@/components/layout/AppLayout'
import IssueWrapper from '@/components/IssueWrapper'
import NewspaperSubscriptionButton from '@/components/widgets/NewspaperSubscriptionButton'
import KairlyPromo from '@/components/KairlyPromo'
import FooterLinks from '@/components/microsite/FooterLinks'
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'
import MoneyFormat from '@/components/widgets/MoneyFormat'

const IMG_REGEXP = /<img[^>]*src="([^"]*)"/g

export default {
  name: 'NewspaperDetail',

  auth: false,

  head() {
    const { title, name, description, picture, editor} = this.newspaper

    let metaTitle
    let metaDescription
    let metaUrl
    let metaPicture
    let images

    if (this.$route.params.issue) {
      //- act as an issue detail
      metaTitle = `${title} #${this.issue.number} – Kairly`
      metaDescription = this.issue.posts
        .map(({post}) => post.content.title || post.author.name)
        .filter(title => title)
        .join(' • ')
        .slice(0, 280)
      metaUrl = `https://kairly.com/${editor.id}/${name}/${this.issue.number}`
    } else {
      //- act as a newspaper detail
      metaTitle = `${title} – Kairly`
      metaDescription = description
      metaUrl = `https://kairly.com/${editor.id}/${name}`
    }

    //- newspaper image
    if (this.$route.params.issue) {
      images = this.issue.posts
        .map(({post}) => IMG_REGEXP.exec(post.content.perex))
        .filter(x => x)
    }

    if (images && images.length) {
      metaPicture = images[0][1]
    } else {
      metaPicture = picture
    }

    const head = {
      title: metaTitle,
      meta: [
        { hid: 'description', name: 'description', content: metaDescription },
        { hid: 'og:title', property: 'og:title', content: metaTitle },
        { hid: 'og:description', property: 'og:description', content: metaDescription },
        { hid: 'og:image', property: 'og:image', content: metaPicture },
        { hid: 'og:image:alt', property: 'og:image:alt', content: title },
        { hid: 'og:type', property: 'og:type', content: 'product' },
        { hid: 'og:url', property: 'og:url', content: metaUrl },
        { hid: 'twitter:card', property: 'twitter:card', content: 'summary' },
        { hid: 'twitter:site', property: 'twitter:site', content: '@kairlynews' },
        { hid: 'twitter:title', property: 'twitter:title', content: metaTitle },
        { hid: 'twitter:description', property: 'twitter:description', content: metaDescription },
        { hid: 'twitter:image', property: 'twitter:image', content: metaPicture },
        { hid: 'author', name: 'author', content: editor.name},
      ],
      link: [
        { rel: 'alternate', type: 'application/rss+xml', title:`${title} - RSS feed`,
          href: `https://kairly.com/${editor.id}/${name}/rss` }
      ]
    }

    if (this.issue) {
      head.meta.push({ hid: `og:article:published_time`, property: 'og:article:published_time', content: this.issue.time})
    }

    return head
  },

  components: {
    AppLayout,
    IssueWrapper,
    NewspaperSubscriptionButton,
    KairlyPromo,
    FooterLinks,
    RecommendButtonIssue,
    MoneyFormat,
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
      const { newspaper, issue, links } = await store.dispatch('getNewspaperDetail', {
        newspaperId: fullName,
        issue: params.issue
      })
      return { newspaper, issue, links }
    } catch (err) {
      error(errorToParams(err))
    }
  },

  async mounted() {
    if (this.loggedIn) {
      await this.$store.dispatch('backlog/loadUserBacklog')
    }
  },
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.newspaper-detail
  position: relative
  padding-bottom: $baseline

  main
    max-width: 900px
    margin: 0 auto


//- Header
.newspaper-detail--header
  position: sticky
  top: -1px
  z-index: 5

  backdrop-filter: blur(10px) saturate(125%)

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: $mobile)
    position: static

  > div
    display: grid
    box-sizing: border-box
    max-width: 900px
    margin: $baseline*0.75 auto
    grid-column-gap: $baseline / 2
    grid-template-areas: "issue-header-image issue-header-title issue-header-subscription" "issue-header-image issue-header-description issue-header-subscription"
    grid-template-columns: $baseline*7 auto $baseline*7
    grid-template-rows: auto auto
    padding: $baseline/4
    overflow: hidden

    font-family: $ff-serif

    @media (max-width: 850px)
      grid-template-areas: "issue-header-title issue-header-subscription" "issue-header-description issue-header-subscription"
      grid-template-columns: auto $baseline*7
      padding-left: $baseline / 2

    @media (max-width: $mobile)
      position: static

      grid-template-areas: "issue-header-title" "issue-header-description" "issue-header-subscription"
      grid-template-columns: 100%

      padding-bottom: 0
      margin: 0

      backdrop-filter: none

    //- Title
    h1
      grid-area: issue-header-title

      font-size: $fs-4
      font-weight: 600
      line-height: $baseline * 1.5
      text-align: center
      text-shadow: 0 0 5px #fafafa

      @media (max-width: 850px)
        text-align: left

      @media (max-width: $mobile)
        font-size: $fs-3

      a
        color: #000

    //- Description
    p
      grid-area: issue-header-description

      text-align: center
      text-shadow: 0 0 2px #fff

      @media (max-width: 850px)
        text-align: left

    //- Picture
    > picture
      grid-area: issue-header-image

      @media (max-width: 850px)
        display: none

      img
        display: block
        height: $baseline * 3
        width: 100%

        object-fit: cover


//- Subscribe
.newspaper-detail--subscribe
  grid-area: issue-header-subscription
  padding: $baseline/4 0

  text-align: center

  @media (max-width: $mobile)
    position: static

  .newspaper-subscription button.to-subscribe,
  .newspaper-subscription button.is-canceled,
  .newspaper-subscription button.is-suspended
    +button(secondary, medium)
    padding: 0
    width: 100%

    @media (max-width: $mobile)
      padding: 0 $baseline/2
      width: auto

  .newspaper-subscription button.is-suspended
    background: lighten($c-base, 10%)
    background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)
    color: #fff

  .newspaper-subscription button.is-subscribed
    +button(primary, medium)
    padding: 0
    width: 100%

    @media (max-width: $mobile)
      padding: 0 $baseline/2
      width: auto

  > p
    color: #555

    font-family: $ff-sans
    font-size: $fs--1
    line-height: 1.42
    text-align: center

    @media (max-width: $mobile)
      display: none

//- Navigation between issues
.newspaper-detail--navigation
  display: grid
  grid-template-columns: auto 1fr auto
  grid-template-areas: "prev-link . next-link"
  padding-top: $baseline / 2
  margin-bottom: -($baseline * 2.375)

  border-top: 1px solid #eee

  a
    position: relative
    z-index: 3

    display: block
    border-radius: 100%
    height: $baseline * 1.5
    width: $baseline * 1.5

    background: #fff
    color: #000

    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: $c-base
      color: #fff

    &.is-disabled
      opacity: 0.5

      cursor: default
      pointer-events: none

      &:hover,
      &:focus
        background: #fff
        color: #000

    &::before
      +fa-icon()
      @extend .fas

    &.previous
      grid-area: prev-link

      &::before
        content: fa-content($fa-var-arrow-left)

    &.next
      grid-area: next-link

      &::before
        content: fa-content($fa-var-arrow-right)


//- Issue
.newspaper-detail--issue
  display: block

  timeline-newspaper
    margin-top: $baseline

  //- That's it...
  > p
    padding: $baseline 0

    border-top: 3px solid #eee

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600
    line-height: 1.42
    text-align: center


//- Footer subscribe to newsletter
.newspaper-detail--newsletter-subscription
  display: table
  margin: 0 auto $baseline/2 auto
  padding: $baseline $baseline 0 $baseline

  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  font-family: $ff-sans

  > h2
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600
    text-align: center

  ul
    display: table
    margin: 0 auto $baseline/2 auto
  
  li
    padding-bottom: $baseline / 4

    list-style: disc outside
    line-height: 1.42

  li a
    color: darken($c-base, 20%)

  //- periodicity
  li .periodicity
    text-transform: lowercase

  li .rss::before
    +fa-icon()

    @extend .fas

    content: fa-content($fa-var-rss-square)

    margin-right: $baseline / 8


  //- author's image
  li img
    height: $baseline * 0.75
    width: $baseline * 0.75
    border-radius: 100%

    vertical-align: middle
    object-fit: cover

  //- Mailchimp
  #mc_embed_signup
    margin-left: auto

    #mc_embed_signup_scroll
      display: flex
      justify-content: center

      @media (max-width: $mobile)
        align-items: center
        flex-direction: column


    input[type=email]
      box-sizing: border-box
      border-radius: 5px 0 0 5px
      height: $baseline * 1.25
      padding: 0 $baseline/4
      margin-bottom: $baseline / 2
      width: 250px

      background: #fff
      border: 1px solid #ddd
      opacity: 0.9

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.25

      transition: 0.15s opacity

      @media (max-width: $mobile)
        border-radius: 5px

      &:focus
        opacity: 1

    input[type=submit]
      box-sizing: border-box
      border-radius: 0 5px 5px 0
      height: $baseline * 1.25
      padding: 0 $baseline
      margin-bottom: $baseline

      background: $c-base
      border: 0
      color: #fff

      cursor: pointer
      font-size: $fs-0
      font-family: $ff-sans
      line-height: $baseline * 1.25

      @media (max-width: $mobile)
        border-radius: 5px

      &:focus,
      &:hover
        background: darken($c-base, 10%)

  #mc-embedded-subscribe-form input[type=checkbox]
    display: inline
    width: auto
    margin-right: 10px

  #mergeRow-gdpr
    margin-top: 20px

  #mergeRow-gdpr fieldset label
    font-weight: normal

  #mc-embedded-subscribe-form .mc_fieldset
    border: none
    min-height: 0px
    padding-bottom: 0px




//- Footer with social buttons
.newspaper-detail--social-sharing
  display: flex
  justify-content: center

  border-top: 3px solid #eee
  padding-top: $baseline / 2

  > a
    margin: 0 $baseline/4

  a.share-fb
    +button-icon($fa-var-facebook, icon, brand)

  a.share-twitter
    +button-icon($fa-var-twitter, icon, brand)

  a.rss
    +button-icon($fa-var-rss-square, icon)

  

//- When newspaper is empty
.newspaper-detail--empty-newspaper
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
