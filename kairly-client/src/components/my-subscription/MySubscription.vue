<template>
  <app-layout>
    <my-subscription-view>
      <nav>
        <router-link :to="{name: 'subscription.editions'}">Editions</router-link>
        <router-link :to="{name: 'subscription.authors'}">Authors</router-link>
      </nav>
      <router-view></router-view>
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

      &.is-active
        color: #000

</style>
