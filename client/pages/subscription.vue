<template>
  <app-layout>
    <my-subscription-view>
      <nav>
        <nuxt-link :to="{name: 'subscription-newspapers'}">Newspapers</nuxt-link>
        <nuxt-link :to="{name: 'subscription-authors'}">Authors</nuxt-link>
      </nav>
      <nuxt-child/>
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
  display: block
  box-sizing: border-box
  max-width: 900px
  margin: $baseline auto
  padding: 0 $baseline/2

  @media (max-width: $mobile)
    padding: 0 $baseline/4

  //- heading
  nav
    margin-bottom: $baseline

    font-size: $fs-2

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 500

      &.nuxt-link-active
        color: #000

</style>
