<template>
  <my-editions-view>
    <h1>My Subscription</h1>
    <nav>
      <router-link :to="{name: 'subscription.editions'}">Editions</router-link> |
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
  h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-2
</style>
