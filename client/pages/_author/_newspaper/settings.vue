<template>
  <AppLayout :name="$t('Edit newspaper')">
    <NewspaperSettings :newspaper="newspaper" />
  </AppLayout>
</template>

<script>
import { mapActions, mapState } from "vuex";

import { errorToParams } from "@/utils/errors"

import AppLayout from '@/components/layout/AppLayout'
import NewspaperSettings from '@/components/editor/NewspaperSettings'

export default {
  name: "NewspaperSettingsPage",

  components: {
    AppLayout,
    NewspaperSettings
  },

  async asyncData({ store, params, error }) {
    const fullName = `${params.author}/${params.newspaper}`

    console.log('asdsad')

    if (store.state.auth.loggedIn) {
      await store.dispatch('getSubscriptions')
    }

    try {
      const { newspaper } = await store.dispatch('getNewspaperDetail', {
        newspaperId: fullName
      })
      return { newspaper }
    } catch (err) {
      error(errorToParams(err))
    }
  }
};
</script>

<style lang="sass">
</style>
