<template>
  <div class="welcome-view">
    
    <section class="welcome-intro">
      <h1>{{ $t('Welcome to Kairly!') }}</h1>

      <!-- <section class="welcome--import">
        <h2>{{ $t('Or import your favorite authors') }}</h2>
        <div class="welcome--import--rss">
          <nuxt-link to="/import">{{  $t('Import RSS feeds')  }}</nuxt-link>

          <p>{{ $t('Upload OPML file.') }}</p>
        </div>

        <div class="welcome--import--twitter">
          <button @click="importTwitter()">
            {{ $t('Read your Twitter on Kairly') }}
          </button>

          <p>{{ $t('Connect your Twitter account.') }}</p>
        </div>
      </section> -->

      <section class="welcome--roles">
        <div>
          <section>
            <h3>{{ $t('As a reader') }}</h3>
            <p>
              {{ $t('Do you want to read newsletters and interesting authors?') }}
            </p>

            <ul>
              <li><a href="#explore-timeline">Subscribe to newsletters</a></li>
              <li><nuxt-link to="/import">Import your RSS feed</nuxt-link></li>
              <li><nuxt-link to="/explore/news">Explore</nuxt-link> or <nuxt-link to="/search">search</nuxt-link></li>
            </ul>
          </section>

          <section>
            <h3>{{ $t('As an editor') }}</h3>
            <p>
              {{ $t('Do you want to start a newsletter and curate content for others?') }}
            </p>

            <ol>
              <li><nuxt-link to="/newspapers">Start a newsletter</nuxt-link></li>
              <li>Curate content for your #1 issue</li>
              <li>Get subscribers and earn money</li>
            </ol>
          </section>

          <section>
            <h3>{{ $t('As an author') }}</h3>
            <p>
              {{ $t('Do you want to start publishing articles and start earning money?') }}
            </p>

            <ol>
              <li><nuxt-link to="/posts">Write a new post</nuxt-link></li>
              <li>Set a price for your content</li>
              <li>Publish it & pitch it to editors</li>
            </ol>
          </section>
        </div>
      </section>
    </section>

    <ExploreTimeline id="explore-timeline" controls="false" />

    <TwitterApologyModal
      :active.sync="isTwitterApologyModalOpen"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import TwitterApologyModal from '@/components/modals/TwitterApologyModal'
import ExploreTimeline from '@/components/ExploreTimeline'

export default {
  name: 'Welcome',

  components: {
    NewspaperWidget,
    TwitterApologyModal,
    ExploreTimeline
  },

  data() {
    return {
      isTwitterApologyModalOpen: false
    }
  },

  methods: {
    importTwitter() {
      this.isTwitterApologyModalOpen = true

      this.$ga.event({
        eventCategory: 'Onboarding / Exploring',
        eventAction: 'Import Twitter',
        eventLabel: 'Welcome screen'
      })
    },

    closeTwitterApology() {
      this.isTwitterApologyModalOpen = false
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- WELCOME VIEW -//
.welcome-view
  display: block
  padding-bottom: $baseline
  max-width: 900px
  margin: 0 auto



.welcome-intro
  padding: $baseline
  background: #fff
  box-shadow: 4px 4px 8px #eee, -4px -4px 8px #fff

    //- Welcome heading
  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center

  //- Sections
  > h2,
  > section > h2
      margin-bottom: $baseline

      font-family: $ff-serif
      font-size: $fs-2
      font-weight: 600
      text-align: center


  ul,
  ol
    margin-top: $baseline

    li
      list-style: disc inside
      margin-bottom: $baseline / 4

      font-weight: 600

      a

        color: darken($c-base, 10%)

        &:hover,
        &:focus
          color: darken($c-base, 20%)

  ol li
    list-style: decimal inside

  //- newspaper crossroad
  .microsite-explore
    > h2
      margin-bottom: 0

  .microsite-explore--crossroad
    margin: 0
    padding: $baseline 0 $baseline/2 0

//- Import
.welcome--import
  display: grid
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto auto
  justify-content: center
  padding: $baseline 0
  margin-bottom: $baseline

  background: #fff
  border: 1px solid #eee

  @media (max-width: $mobile)
    grid-template-columns: auto
    grid-template-rows: auto auto auto
    grid-row-gap: $baseline / 2

  > h2
    grid-column: 1 / span 2

    @media (max-width: $mobile)
      grid-column: 1
      margin-bottom: 0 !important

  > div
    grid-row: 2
    margin: 0 $baseline*2

    text-align: center

    @media (max-width: $mobile)
      grid-row: auto

  p
    font-size: $fs--1

  .welcome--import--twitter
    button
      +button-icon($fa-var-twitter, icon-text, brand)

  .welcome--import--rss
    a
      +button-icon($fa-var-rss, icon-text, solid)


//- Roles
.welcome--roles

  > div
    display: flex

    @media (max-width: $mobile)
      flex-direction: column
      padding: 0 $baseline/4
      margin-bottom: 0

  section
    position: relative

    flex: 1
    margin-right: $baseline * 1.5

    @media (max-width: $mobile)
      margin: 0 0 $baseline 0

    &:last-of-type
      margin-right: 0

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-2
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

  h3 + p
   

  p + p
    margin-top: $baseline / 2

    @media (max-width: $mobile)
      margin-top: $baseline / 4

    a
      color: $c-base

      font-weight: 600

      transition: .15s all

      &:hover
        color: darken($c-base, 10%)

      &::after
        +fa-icon()
        @extend .fas

        margin-left: $baseline / 2

        opacity: 0.5

        content: fa-content($fa-var-arrow-right)


      &:hover::after
        opacity: 1

  //- start reading Kairly button
  > a
    +button(primary, large)

    display: table
    margin: 0 auto

</style>
