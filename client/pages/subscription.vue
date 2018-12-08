<template>
  <app-layout>
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
          <li><a href="">Malostranské noviny</a></li>
          <li><a href="">Deník Aktuálně - Domací</a></li>
          <li><a href="">Hospodářské noviny</a></li>
          <li><a href="">Technologický deník</a></li>
          <li><a href="">iRozhlas - zprávy z domova</a></li>
        </ul>

        <h3>{{ $t('New authors on Kairly') }}</h3>
        <ul>
          <li><a href="">ČTK</a></li>
          <li><a href="">Deník N</a></li>
          <li><a href="">Neovlivni.cz</a></li>
          <li><a href="">Investigace.cz</a></li>
          <li><a href="">Janův blog</a></li>
        </ul>

        <p>{{ $t('You can find more newspapers and authors on Explore page.') }}</p>

        <p><a href="">{{ $t('Explore more content') }}</a></p>
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
}
</script>

<style lang="sass">
my-subscription-view
  display: grid
  grid-column-gap: $baseline
  grid-template-columns: 2fr 1fr
  grid-template-rows: auto auto
  grid-template-areas: "subscription-nav subscription-explore" "subscription-main subscription-explore"

  box-sizing: border-box
  max-width: 900px
  margin: $baseline auto

  @media (max-width: $mobile)
    padding: 0 $baseline/4

  //- Switcher
  > nav
    grid-area: subscription-nav
    margin-bottom: $baseline

    font-size: $fs-3

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 600

      &.nuxt-link-active
        color: #000

  //- Main view
  > main
    grid-area: subscription-main

  //- Explore promotion
  > aside
    grid-area: subscription-explore

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
