<template>
  <app-layout :name="$t('Subscriptions')">
    <my-subscription-view>
      <nav>
        <nuxt-link :to="{name: 'subscription-newspapers'}">{{ $t('Newspapers') }}</nuxt-link>
        <nuxt-link :to="{name: 'subscription-authors'}">{{ $t('Authors') }}</nuxt-link>
      </nav>

      <main>
        <nuxt-child/>
      </main>

      <aside>
        <h2>{{ $t('Explore') }}</h2>

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

        <p><nuxt-link to="/explore">{{ $t('Explore more content') }}</nuxt-link></p>
      </aside>

    </my-subscription-view>
  </app-layout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'MySubscription',

  components: {
    AppLayout
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
my-subscription-view
  display: grid
  grid-column-gap: $baseline
  grid-template-columns: 2fr 1fr
  grid-template-rows: auto auto
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
        color: #000

  //- Main view
  > main
    grid-area: subscription-main

  //- Explore promotion
  > aside
    grid-area: subscription-explore

    @media (max-width: 800px)
      display: none

    h2
      margin-bottom: $baseline

      font-size: $fs-3
      font-weight: 600

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

</style>
