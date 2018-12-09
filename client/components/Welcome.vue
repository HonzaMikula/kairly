<template>
  <timeline-welcome>
    <div class="welcome-view">
      <h1>{{ $t('Welcome to Kairly!') }}</h1>

      <section class="welcome--topics">
        <h2>{{ $t('Start with subscribing to newspapers') }}</h2>

        <ul>
          <li v-for="topic in topics" :key="topic.name">
            <a href="" @click.stop.prevent="selectTopic(topic)" :class="{'is-active': selectedTopic === topic}">{{ topic.name }}</a>
          </li>
        </ul>
      </section>

      <section class="welcome--newspapers">
        <loading-spinner v-if="loading"></loading-spinner>
        <div v-else>
          <NewspaperWidget
            v-for="newspaper in newspapers"
            :key="newspaper.fullName"
            :newspaper="newspaper"
          />
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

    </div>
  </timeline-welcome>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import TABS from '@/exploreTabs'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'

export default {
  name: 'Welcome',

  components: {
    NewspaperWidget
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
      newspapers: []
    }
  },

  methods: {
    async selectTopic(topic) {
      this.selectedTopic = topic
      this.loading = true
      this.newspapers = await this.$store.dispatch('getNewspapers', topic.newspapers)
      this.loading = false
    }
  },

  async created() {
    this.newspapers = await this.$store.dispatch('getNewspapers', this.selectedTopic.newspapers)
    this.loading = false
  }
}
</script>

<style lang="sass">
//- Welcome view
.welcome-view
  display: block

  //- Welcome heading
  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center

  //- Sections
  > section > h2
      margin-bottom: $baseline

      font-family: $ff-serif
      font-size: $fs-2
      font-weight: 600
      text-align: center


//- Topics
.welcome--topics
  margin-bottom: 0

  ul
    display: flex
    justify-content: center
    margin-bottom: $baseline / 2

  li
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

  > div
    display: grid
    grid-row-gap: $baseline / 2
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2

    @media (max-width: $mobile)
      grid-column-gap: $baseline / 4
      overflow-x: auto

      newspaper-widget-view
        min-width: 200px


//- Roles
.welcome--roles

  > div
    display: flex
    margin-bottom: $baseline * 2

    @media (max-width: $mobile)
      flex-direction: column

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

  p + p
    margin-top: $baseline / 2

    a
      color: $c-base

      font-weight: 600

      transition: .15s all

      &:hover
        color: darken($c-base, 10%)

      &::after
        +fa-icon()

        margin-left: $baseline / 2

        opacity: 0.5

        content: $fa-var-arrow-right


      &:hover::after
        opacity: 1

  //- start reading Kairly button
  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
