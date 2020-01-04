<template>
  <div class="welcome-view">
    
    <section class="welcome-intro">
      <h1>{{ $t('Welcome to Kairly!') }}</h1>

      <div class="welcome-intro--roles">
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

    <nav class="welcome--explore-tabs">
      <ul>
        <li 
          v-for="tab in tabs" 
          :key="tab.slug"
          :class="{'is-active': tab == currentTab}">
          <a href @click.prevent="switchTab(tab)">
            {{ tab[$i18n.locale] || tab.en }}
          </a>
        </li>
      </ul>
    </nav>

    <ExploreTimeline id="explore-timeline" disableControls :category="currentTab" />

  </div>
</template>

<script>
import TABS from '@/exploreTabs'
import ExploreTimeline from '@/components/ExploreTimeline'

export default {
  name: 'Welcome',

  components: {
    ExploreTimeline
  },

  data() {
    return {
      tabs: TABS,
      currentTab: TABS.find(t => t.slug === 'news')
    }
  },

  methods: {
    switchTab(tab) {
      this.currentTab = tab

      this.$ga.event({
        eventCategory: 'Onboarding',
        eventAction: 'Switch timeline',
        eventLabel: tab
      })
    }
  }
}
</script>

<style lang="sass">
//- WELCOME VIEW -//
.welcome-view
  display: block
  padding-bottom: $baseline
  max-width: 900px
  margin: 0 auto

//- Intro Box
.welcome-intro
  padding: $baseline
  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

    //- Welcome heading
  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center


//- Roles
.welcome-intro--roles
  display: grid
  grid-auto-columns: 1fr
  grid-auto-flow: column
  grid-column-gap: $baseline

  @media (max-width: $mobile)
    grid-auto-flow: row

  section
    position: relative

    display: flex
    flex-direction: column

    @media (max-width: $mobile)
      margin: 0 0 $baseline 0

      &:last-of-type
        margin-bottom: 0

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-2
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

  h3 + p
    margin-bottom: auto

  ul,
  ol
    margin-top: $baseline
    
    @media (max-width: $mobile)
      margin-top: $baseline / 2

    li
      list-style: disc outside
      margin-bottom: $baseline / 4
      margin-left: $baseline * 0.75

      font-weight: 600
      line-height: 1.42

      a

        color: darken($c-base, 10%)

        &:hover,
        &:focus
          color: darken($c-base, 20%)

  ol li
    list-style: decimal outside

//- Tabs
.welcome--explore-tabs
  margin: $baseline $baseline 0 $baseline

  ul
    display: flex
    justify-content: center

    @media (max-width: $mobile)
      display: block

      white-space: nowrap
      overflow-x: auto
      -webkit-overflow-scrolling: touch

  li
    margin-right: $baseline

    font-size: $fs-2

    @media (max-width: $mobile)
      display: inline-block

    &:last-of-type
      margin-right: 0

    &.is-active 
      font-weight: 600

    a
      color: #000
</style>
