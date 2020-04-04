<template>
  <AppLayout>
    <div class="error-page">
      <template v-if="error.statusCode === 404">
        <h1>Sorry, but this page doesn't exist</h1>
      </template>

      <template v-else>
        {{ error.message || 'Oops' }}
      </template>

      <p>
        <a href="#" @click="$router.go(-1)">Return back</a>
        or
        <nuxt-link to="/">Go to the homepage</nuxt-link>
      </p>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'

export default {

  components: {
    AppLayout
  },

  props: {
    error: { type: Object, required: true }
  }
}
</script>

<style lang="sass">
.error-page
  padding-top: $baseline * 4
  text-align: center

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  a
    display: inline-block
    border-radius: 5px
    padding: 0 $baseline/2

    background: $c-base
    border: 1px solid $c-base
    color: #fff

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0
    line-height: $baseline

    &:focus,
    &:hover
      background: darken($c-base, 10%)

</style>
