<template>
  <div class="welcome-view">
    <h1>{{ $t('Welcome to Kairly!') }}</h1>

    <ExploreNewspapers>
      {{ $t('Subscribe to newspapers prepared by professional editors') }}
    </ExploreNewspapers>

    <section class="welcome--import">
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
    </section>

    <section class="welcome--roles">
      <h2>{{ $t('Start using Kairly') }}</h2>
      <div>
        <section>
          <h3>{{ $t('As a reader') }}</h3>
          <p>
            {{ $t('Are you interested in more newspapers and authors?') }}
          </p>
          <p><nuxt-link to="/explore">{{ $t('Explore more content') }}</nuxt-link></p>
        </section>

        <section>
          <h3>{{ $t('As an editor') }}</h3>
          <p>
            {{ $t('Do you want to start a newspaper and pick the best content for others?') }}
          </p>

          <p><nuxt-link to="/newspapers">{{ $t('Start a newspaper') }}</nuxt-link></p>
        </section>

        <section>
          <h3>{{ $t('As an author') }}</h3>
          <p>
            {{ $t('Do you want to start writing articles and tweets?') }}
          </p>

          <p><nuxt-link to="/posts">{{ $t('Write a new post') }}</nuxt-link></p>
        </section>
      </div>

      <a href="" @click.prevent="$router.go({path:'/', force: true})">{{ $t('Go Home to start reading') }}</a>
    </section>

    <TwitterApologyModal
      :active.sync="isTwitterApologyModalOpen"
    />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import TABS from '@/exploreTabs'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import TwitterApologyModal from '@/components/modals/TwitterApologyModal'
import ExploreNewspapers from '@/components/microsite/ExploreNewspapers'

export default {
  name: 'Welcome',

  components: {
    NewspaperWidget,
    TwitterApologyModal,
    ExploreNewspapers
  },

  data() {
    const topics = TABS.map(t => ({
      name: t.name === 'Best of Kairly' ? 'All topics' : t.name,
      newspapers: t.newspapers
    }))

    return {
      topics,
      selectedTopic: topics[0],
      loading: true,
      newspapers: [],
      isTwitterApologyModalOpen: false
    }
  },

  methods: {
    async selectTopic(topic) {
      this.selectedTopic = topic
      this.loading = true
      this.newspapers = await this.$store.dispatch('getNewspapers', topic.newspapers)
      this.loading = false
    },

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
  },

  async created() {
    this.newspapers = await this.$store.dispatch('getNewspapers', this.selectedTopic.newspapers)
    this.loading = false
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

//- Topics
.welcome--topics
  margin-bottom: 0

  ul
    display: flex
    justify-content: center
    margin-bottom: $baseline / 2
    padding: 0 $baseline/4

    @media (max-width: $mobile)
      display: block

      white-space: nowrap
      overflow-x: auto
      -webkit-overflow-scrolling: touch

  li
    display: inline-block
    margin-right: $baseline / 2

  a
    display: block
    border-radius: 5px

    color: $c-base

    font-weight: 600
    font-size: $fs-1

    &:hover,
    &:focus
      color: darken($c-base, 10%)

    &.is-active
      color: #000

//- Newspapers
.welcome--newspapers
  margin-bottom: $baseline * 2
  padding: 0 $baseline/4

  @media (max-width: $mobile)
    margin-bottom: $baseline

  > div
    display: grid
    grid-row-gap: $baseline / 2
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2

    @media (max-width: $mobile)
      grid-column-gap: $baseline / 4
      overflow-x: auto
      -webkit-overflow-scrolling: touch

      .newspaper-widget-view
        min-width: 200px

//- Illustration on newspaper widget
.welcome--newspapers--loading
  border-radius: 5px
  padding: $baseline / 4

  background: #fff
  border: 1px solid #eee

  text-align: center

  //- picture
  .picture
    height: 120px
    margin-bottom: $baseline / 2
    background: #eee

  //- title
  .title
    height: $baseline / 2
    margin-bottom: $baseline / 4
    width: 75%
    background: #eee

  p
    margin-bottom: $baseline / 2
    color: #999
    font-family: $ff-sans
    font-size: $fs--1
    font-weight: 600
    line-height: $baseline * 0.8
    text-align: left

  //- description
  .description
    &::after,
    &::before
      display: block
      height: $baseline / 4
      margin-bottom: $baseline / 4
      border-bottom: $baseline / 4 solid #eee
      border-top: $baseline / 4 solid #eee
      content: ''

  //- subscribe
  .subscribe
    display: inline-block
    border-radius: $baseline
    margin: 0 auto
    padding: 0 $baseline/2
    border: 1px solid #eee
    color: #999
    font-family: $ff-sans
    font-size: $fs--1

//- Roles
.welcome--roles

  > div
    display: flex
    margin-bottom: $baseline * 2

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
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

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
