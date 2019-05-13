<template>
  <AppLayout :name="$t('Import')">
    <div class="import-view">
      <h1>Feeds to import</h1>

      <table>
        <thead>
          <tr>
            <th><input type="checkbox" checked name="" @change="selectAll($event)" /></th>
            <th>Name</th>
            <th>When to display new posts?</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="source in sources" :key="source.xmlUrl">
            <td>
              <input
                v-model="source.selected"
                type="checkbox"
                name=""
              />
            </td>
            <th>
              {{ source.title }}
              </th>
            <td>
              <template v-if="isKairlyNewspaper(source.xmlUrl)">
                Subscribe to the newspaper
              </template>
              <template v-else>
                <a href="" @click.prevent.stop="changePerodicityTarget = source; showChangePeriodicityDialog = !showChangePeriodicityDialog">
                  {{ getPeriodicityLabel(source.periodicity) }}
                </a>
              </template>
            </td>
          </tr>
        </tbody>
      </table>

      <ChangePeriodicity
        v-if="showChangePeriodicityDialog"
        @changePeriodicity="changePeriodicity"
      />

      <button @click="submit">Import feeds</button>
    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import ChangePeriodicity from '@/components/widgets/ChangePeriodicity'

export default {
  name: 'Settings',

  components: {
    AppLayout,
    ChangePeriodicity,
  },

  mixins: [PeriodicityMixin],

  head() {
    return {
      title: this.$t('System Reports')
    }
  },

  data() {
    return {
      showChangePeriodicityDialog: false,
      changePerodicityTarget: null,
      sources: this.$store.state.opml.map(source => {
        const newpspaper = this.isKairlyNewspaper(source.xmlUrl)
        return {
          ...source,
          newpspaper,
          selected: true,
          periodicity: newpspaper ? null : {frequency: '6x_per_day'}
        }
      })
    }
  },

  methods: {
    selectAll(ev) {
      const value = ev.target.checked
      this.sources.forEach(s => s.selected = value)
    },

    changePeriodicity(frequency, dow, time) {
      this.changePerodicityTarget.periodicity = {
        "frequency": frequency,
        "dow": dow,
        "time": time
      }
      this.showChangePeriodicityDialog = false
      this.changePerodicityTarget = null
    },

    isKairlyNewspaper(url) {
      return url.match('://kairly.com/[^/]+/[^/]+/rss')
    },

    async submit() {
      const sources = this.sources
        .filter(s => s.selected)
        .map(s => ({title: s.title, url: s.xmlUrl, periodicity: s.periodicity}))
      await this.$axios.$post(`/import-rss`, {sources})
      //this.$router.push("/")
    }
  },

  fetch ({ store, redirect }) {
    if (store.state.opml === null) {
      redirect('/')
    }
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
