<template>
  <AppLayout :name="$t('Newspaper detail')">
    <div class="newspaper-detail" itemtype="https://schema.org/Newspaper" itemscope>
      <header class="newspaper-detail--header">
        <h1 itemprop="name"><nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">{{ newspaper.title }}</nuxt-link></h1>
        <p>{{ newspaper.description }}</p>

        <picture itemprop="image">
          <img
            v-if="newspaper.picture"
            :src="newspaper.picture"
            :alt="newspaper.title"
          />
          <div v-else class="image-placeholder"></div>
        </picture>

        <div class="newspaper-detail--subscribe" v-if="loggedIn">
          <NewspaperSubscription :newspaper="newspaper" />

          <p>{{ periodicity }}</p>
        </div>
      </header>

      <div class="newspaper-detail--info">
        <ul>
          <li>{{ periodicity }}</li>
          <li class="issues">#{{ newspaper.issues }}</li>
          <li>{{ newspaper.likes }} {{ $t('readers') }}</li>
          <li itemprop="editor" itemscope itemtype="http://schema.org/Person">{{ newspaper.editor.name }}</li>
          <li class="price">
            <MoneyFormat :value="newspaper.price" currency="Kč" :short="true" />
            {{ $t('monthly') }}
          </li>
        </ul>
      </div>

      <template v-if="issue">
        <nav class="newspaper-detail--navigation" v-if="links.prev || links.next">
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
          <IssueWrapper :issue="issue" :subscription="newspaper.subscription" hideDate showTail>
            <template slot="newspaperTitle">{{ $t('Issue from') }} <time itemprop="datePublished">{{ issue.time | moment('D. M. YYYY')}}</time></template>
          </IssueWrapper>
        </div>

        <footer class="newspaper-detail--social-sharing">
          <a
            :href="`https://kairly.com/${newspaper.editor.id}/${newspaper.name}/rss`"
            target="_blank"
            class="rss"
            :aria-label="$t('Subscribe RSS')"
            @click="$ga.event({
              eventCategory: 'Subscribe RSS newspaper',
              eventAction: newspaper.name,
              eventLabel: newspaper.editor.id
            })"
          />

          <a
            :href="`https://www.facebook.com/sharer/sharer.php?u=https://kairly.com/${issue.id}`"
            target="_blank"
            class="share-fb"
            :aria-label="$t('Share on Facebook')"
            @click="$ga.event({
              eventCategory: 'Share newspaper FB',
              eventAction: newspaper.name,
              eventLabel: newspaper.editor.id
            })"
          />

          <a
            :href="`https://twitter.com/intent/tweet?url=https://kairly.com/${issue.id}&text=${newspaper.title}`"
            target="_blank"
            class="share-twitter"
            :aria-label="$t('Share on Twitter')"
            @click="$ga.event({
              eventCategory: 'Share newspaper Twitter',
              eventAction: newspaper.name,
              eventLabel: newspaper.editor.id
            })"
          />

          <!-- Begin Mailchimp Signup Form -->
          <div id="mc_embed_signup" v-if="newspaper.newsletterSubscriptionUrl">
            <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
              <div id="mc_embed_signup_scroll">
                <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" :placeholder="$t('email address')" required>
                <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
                <div style="position: absolute; left: -5000px;" aria-hidden="true">
                  <input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value="">
                  <input type="checkbox" :value="newspaper.newsletterSubscriptionUrl" :name="`group[84705][${newspaper.newsletterSubscriptionUrl}]`" checked />
                </div>
                <div class="clear">
                  <input
                    id="mc-embedded-subscribe"
                    type="submit"
                    :value="$t('Send newspaper by email')"
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
          <!--End mc_embed_signup-->
        </footer>
      </template>

      <div class="newspaper-detail--empty-newspaper" v-else>
        <h2>{{ $t('No issue yet') }}</h2>
        <p>
          {{ $t('Subscribe the newspaper and once it\'s published, we will show you on your timeline.') }}
        </p>
      </div>
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
import NewspaperSubscription from '@/components/widgets/NewspaperSubscription'
import KairlyPromo from '@/components/KairlyPromo'
import FooterLinks from '@/components/microsite/FooterLinks'
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'
import MoneyFormat from '@/components/widgets/MoneyFormat'

export default {
  name: 'NewspaperDetail',

  auth: false,

  head() {
    const { title, name, description, picture, editor} = this.newspaper

    let metaTitle
    let metaDescription
    let metaUrl

    //- act as an issue detail
    if (this.$route.params.issue) {
      metaTitle = `${title} #${this.issue.number} – Kairly`
      metaDescription = this.issue.posts
        .map(post => post.content.title || post.author.name)
        .filter(title => title)
        .join(' • ')
        .slice(0, 280)
      metaUrl = `https://kairly.com/${editor.id}/${name}/${this.issue.number}`
    }
    //- act as a newspaper detail
    else {
      metaTitle = `${title} – Kairly`
      metaDescription = description
      metaUrl = `https://kairly.com/${editor.id}/${name}`
    }

    return {
      title: metaTitle,
      meta: [
        { hid: 'description', name: 'description', content: metaDescription },
        { hid: 'og:title', property: 'og:title', content: metaTitle },
        { hid: 'og:description', property: 'og:description', content: metaDescription },
        { hid: 'og:image', property: 'og:image', content: picture },
        { hid: 'og:image:alt', property: 'og:image:alt', content: title },
        { hid: 'og:type', property: 'og:type', content: 'product' },
        { hid: 'og:url', property: 'og:url', content: metaUrl },
        { hid: 'twitter:card', property: 'twitter:card', content: 'summary' },
        { hid: 'twitter:site', property: 'twitter:site', content: '@kairlynews' },
        { hid: 'twitter:title', property: 'twitter:title', content: metaTitle },
        { hid: 'twitter:description', property: 'twitter:description', content: metaDescription },
        { hid: 'twitter:image', property: 'twitter:image', content: picture },
      ],
      link: [
        { rel: 'alternate', type: 'application/rss+xml', title:`${title} - RSS feed`,
          href: `https://kairly.com/${editor.id}/${name}/rss` }
      ]
    }
  },

  components: {
    AppLayout,
    IssueWrapper,
    NewspaperSubscription,
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
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.newspaper-detail
  position: relative

  margin: 0 auto
  max-width: 900px
  padding-bottom: $baseline


//- Header
.newspaper-detail--header
  position: sticky
  top: -1px
  z-index: 5

  display: grid
  grid-column-gap: $baseline / 2
  grid-template-areas: "issue-header-image issue-header-title issue-header-subscription" "issue-header-image issue-header-description issue-header-subscription"
  grid-template-columns: $baseline*7 auto $baseline*7
  grid-template-rows: auto auto
  padding: $baseline/4 0
  margin: $baseline*0.75 0
  overflow: hidden

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

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

//- Info row about newspaper
.newspaper-detail--info
  display: block
  padding: $baseline/4 0

  border-bottom: 1px solid #ddd
  border-top: 1px solid #ddd

  ul
    display: table
    margin: 0 auto

    @media (max-width: $mobile)
      padding: 0 $baseline/4

  li
    display: inline-block

    font-size: $fs--1
    font-family: $ff-serif
    vertical-align: middle

    &::after
      display: inline-block
      padding: 0 $baseline/2

      content: '•'

      @media (max-width: $mobile)
        padding: 0 $baseline/4

    &:last-of-type::after
      display: none

    @media (max-width: $mobile)
      &.issues,
      &.price
        display: none

      &:nth-of-type(4)::after
        display: none

//- Navigation between issues
.newspaper-detail--navigation
  display: grid
  grid-template-columns: auto 1fr auto
  grid-template-areas: "prev-link . next-link"
  padding-top: $baseline / 2
  margin-bottom: -($baseline * 2.375)

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
    +button-icon($fa-var-rss-square, icon-text)

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
      height: $baseline * 1.5
      padding: 0 $baseline/2
      margin-bottom: $baseline / 2
      width: 250px

      background: #fff
      border: 1px solid #ddd
      opacity: 0.9

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.5

      transition: 0.15s opacity

      @media (max-width: $mobile)
        border-radius: 5px

      &:focus
        opacity: 1

    input[type=submit]
      box-sizing: border-box
      border-radius: 0 5px 5px 0
      height: $baseline * 1.5
      padding: 0 $baseline
      margin-bottom: $baseline

      background: $c-base
      border: 0
      color: #fff

      cursor: pointer
      font-size: $fs-1
      font-family: $ff-sans
      line-height: $baseline * 1.5

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
