<template>
  <AppLayout :name="$t('Start newsletter')">
    <NewspaperSettings />
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import NewspaperSettings from '@/components/editor/NewspaperSettings'

export default {
  name: 'NewspaperSettingsPage',

  components: {
    AppLayout,
    NewspaperSettings
  }
}
</script>

<style lang="sass">
</style>
