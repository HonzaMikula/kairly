<template>
  <div class="not-found">
    <h1 v-if="error.statusCode === 404">Page not found</h1>
    <h1 v-else>{{ error.message || 'Oops' }}</h1>
  </div>
</template>

<script>
export default {
  props: ['error']
}
</script>

<style lang="sass">
.not-found
  padding-top: $baseline * 4
  text-align: center
  font-size: $fs-2

</style>
