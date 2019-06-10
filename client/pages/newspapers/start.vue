<template>
  <AppLayout :name="$t('Start newspaper')">
    <NewspaperSettings />
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
  }
};
</script>

<style lang="sass">
</style>
