<template>
  <AppLayout :name="$t('Import')">
    <div class="import-view">
      <h1>Feeds to import</h1>

      <table>
        <thead>
          <tr>
            <th><input type="checkbox" checked name="" /></th>
            <th>Name</th>
            <th>When to display new posts?</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="source in sources" :key="source.xmlUrl">
            <td><input type="checkbox" checked name="" /></td>
            <th>{{ source.title }}</th>
            <td>Every 3 hours</td>
          </tr>
        </tbody>
      </table>

      <button>Import feeds</button>
    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'Settings',

  head() {
    return {
      title: this.$t('System Reports')
    }
  },

  computed: mapState({
    sources: state => state.opml,
  }),

  components: {
    AppLayout
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

//- Import
.import-view
  margin: $baseline auto
  max-width: 900px

  > h1
    margin-bottom: $baseline / 2

    font-size: $fs-2
    font-weight: 600

  //- Table
  table
    margin-bottom: $baseline

    background: #fff
    border: 1px solid #eee

  td,
  th
    padding: $baseline / 4
    padding-right: $baseline

  td:first-child,
  th:first-child
    padding-right: $baseline / 4

  thead th
    border-bottom: 1px solid #eee

    font-weight: 600
    text-align: left

  tbody td,
  tbody th
    border-bottom: 1px solid #eee

    text-align: left

  // Submit Button
  > button
    +button

</style>
