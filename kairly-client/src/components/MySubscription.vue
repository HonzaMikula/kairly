<template>
  <my-editions-view>
    <nav>
      <router-link :to="{name: 'subscription.editions'}">Editions</router-link>
      <router-link :to="{name: 'subscription.authors'}">Authors</router-link>
    </nav>
    <router-view></router-view>
  </my-editions-view>
</template>

<script>
export default {
  name: 'MySubscription'
}
</script>

<style lang="sass">
my-editions-view
  display: block
  max-width: 900px
  margin: $baseline auto

  @media (max-width: $mobile)
    padding: 0 $baseline

  //- wrapper
  > div
    display: flex
    flex-wrap: wrap
    margin: 0 -$baseline/4

  //- heading
  nav
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-2

    a
      display: inline-block
      margin-right: $baseline

      color: $c-base

      font-weight: 600
      text-decoration: none

      &.is-active
        color: #000

</style>
