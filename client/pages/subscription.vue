<template>
  <AppLayout :name="$t('Subscriptions')">
    <my-subscription-view>
      <nav>
        <nuxt-link :to="{name: 'subscription-newspapers'}">{{ $t('Newspapers') }}</nuxt-link>
        <nuxt-link :to="{name: 'subscription-authors'}">{{ $t('Authors') }}</nuxt-link>
      </nav>

      <main>
        <nuxt-child/>
      </main>

      <aside>
        <section class="subscription--credits">
          <h2><nuxt-link to="/user/transactions/history">{{ $t('Credits') }}</nuxt-link></h2>
          <p>{{ $t('Current balance') }}</p>
          <p class="credits">
            <MoneyFormat :value="user.credits" currency="Kč" :short="true"/>
          </p>

          <p>{{ $t('Monthly spending') }}</p>
          <p class="credits">
            <MoneyFormat :value="monthSpending" currency="Kč" :short="true"/>
          </p>
          <nuxt-link to="/user/add-credits">
            <button>{{ $t('Buy credits') }}</button>
          </nuxt-link>
        </section>

        <section class="subscription--imports">
          <h2>{{ $t('Import authors') }}</h2>

          <h3>{{ $t('Import RSS feeds') }}</h3>

          <WelcomeImportRss @loaded="$router.push('/import')" />

          <h3>{{ $t('Read your Twitter on Kairly') }}</h3>
          <p>{{ $t('Connect to your Twitter account and read your timeline on Kairly.') }}</p>
          <button>{{ $t('Connect to your Twitter') }}</button>
        </section>

        <section>
          <h2><nuxt-link to="/explore">{{ $t('Explore') }}</nuxt-link></h2>

          <h3>{{ $t('Recent newspaper issue') }}</h3>
          <ul>
            <li
              v-for="issue in issues"
              :key="`${issue.newspaper.fullName}#${issue.number}`"
            >
              <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: issue.newspaper.editor.id, newspaper: issue.newspaper.name, issue: issue.number}}">
                {{ issue.newspaper.title }}
              </nuxt-link>
            </li>
          </ul>

          <h3>{{ $t('New authors on Kairly') }}</h3>
          <ul>
            <li v-for="author in authors" :key="author.id">
              <nuxt-link :to="{name: 'author', params: {author: author.id}}">
                {{ author.name }}
              </nuxt-link>
            </li>
          </ul>

          <p>{{ $t('You can find more newspapers and authors on Explore page.') }}</p>

          <p class="explore-more-content"><nuxt-link to="/explore">{{ $t('Explore more content') }}</nuxt-link></p>
        </section>
      </aside>
    </my-subscription-view>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import { mapGetters, mapState, mapActions } from 'vuex'

import MoneyFormat from '@/components/widgets/MoneyFormat'
import WelcomeImportRss from '@/components/widgets/WelcomeImportRss'

export default {
  name: 'MySubscription',

  components: {
    AppLayout,
    MoneyFormat,
    WelcomeImportRss
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    }),
    ...mapGetters(['monthSpending']),
  },

  async asyncData({ app }) {
    const [issues, best_of] = await Promise.all([
      app.$axios.$get('/recent/issues?count=5'),
      app.$axios.$get('/explore/Best of Kairly')  // hack using best of tab, which contains new authors
    ])
    const authors = best_of.categories[1].authors.slice(0, 5)
    return { issues, authors }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Subscription View -//  
my-subscription-view
  display: grid
  grid-column-gap: $baseline
  grid-template-columns: 2fr 1fr
  grid-template-rows: min-content 1fr
  grid-template-areas: "subscription-nav subscription-explore" "subscription-main subscription-explore"

  padding: 0 $baseline
  max-width: 900px
  margin: $baseline auto

  @media (max-width: 800px)
    grid-template-columns: 2fr
    grid-template-areas: "subscription-nav" "subscription-main" "subscription-explore"

  @media (max-width: $mobile)
    padding: 0 $baseline/4
    margin: $baseline/2 auto

  //- Switcher
  > nav
    grid-area: subscription-nav
    margin-bottom: $baseline

    font-size: $fs-3

    @media (max-width: $mobile)
      margin-bottom: $baseline / 2

      font-size: $fs-2

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 600

      @media (max-width: $mobile)
        margin-right: $baseline / 2

      &.nuxt-link-active
        border-bottom: 2px solid #000
        color: #000

  //- Main view
  > main
    grid-area: subscription-main

  //- Explore promotion
  > aside
    grid-area: subscription-explore

    @media (max-width: 800px)
      display: none

    //- add credits
    button
      +button-text 


    section
      margin-bottom: $baseline

    .subscription--credits
      //- info about credits
      .credits
        margin-bottom: $baseline / 2
        font-size: $fs-1
        font-weight: 600

      //- add credits
      button
        +button-text

    .welcome--import--rss
      margin-bottom: $baseline

    h2
      margin-bottom: $baseline

      font-size: $fs-3
      font-weight: 600

      a
        color: #000

    h3
      margin-bottom: $baseline / 2
      font-size: $fs-1
      font-weight: 600

    //- list of authors & newspapers
    ul
      margin-bottom: $baseline

    li
      list-style: disc inside

      a
        color: #555

        &:hover,
        &:focus
          color: #000

    //- promotion for Explore page
    .explore-more-content
      margin-top: $baseline / 2

      a
        +button-text

//- Section import
.subscription--imports
  margin-bottom: 0

  button
    +button-text

    margin-bottom: $baseline
</style>
