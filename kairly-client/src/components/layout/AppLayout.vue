<template>
  <app-main>
    <app-header />
    <slot></slot>
  </app-main>
</template>

<script>

import AppHeader from '@/components/layout/Header'

export default {
  name: 'AppLayout',
  components: {
    AppHeader
  },
}
</script>

<style lang="sass">
</style>
