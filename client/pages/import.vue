<template>
  <AppLayout :name="$t('Import')">
    <div v-if="sources === null">
      <WelcomeImportRss style="margin: auto; width: 300px; margin-top: 40px" />
    </div>
    <div
      v-else
      class="import-view"
    >
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

      <div v-if="importing">
        {{ progress }} / {{ progressTotal }}
        <loading-spinner></loading-spinner>
      </div>
      <button
        v-else
        @click="submit">Import feeds
      </button>
    </div>
  </AppLayout>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import ChangePeriodicity from '@/components/widgets/ChangePeriodicity'
import WelcomeImportRss from '@/components/widgets/WelcomeImportRss'

export default {
  name: 'Settings',

  components: {
    AppLayout,
    ChangePeriodicity,
    WelcomeImportRss,
  },

  mixins: [PeriodicityMixin],

  head() {
    return {
      title: this.$t('System Reports')
    }
  },

  data() {
    return {
      importing: false,
      progress: null,
      progressTotal: null,
      showChangePeriodicityDialog: false,
      changePerodicityTarget: null,
    }
  },

  computed: {
    sources() {
      const { opml } = this.$store.state
      if (!opml) {
        return null
      }
      return opml.map(source => {
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
    ...mapActions(['subscribeAuthor', 'subscribeNewspaper']),

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
      return url.match('://kairly\\.com/[^/]+/[^/]+/rss$')
    },

    async submit() {
      const sources = this.sources
        .filter(s => s.selected)
        .map(s => ({title: s.title, xmlUrl: s.xmlUrl, htmlUrl: s.htmlUrl, periodicity: s.periodicity}))

      if (sources.length) {
        const targets = []

        this.importing = true
        this.progress = 0
        this.progressTotal = sources.length + 1  // one to step for final subscribe


        for (const source of sources) {
          const data = await this.$axios.$post(`/import-rss`, {source})
          this.progress += 1
          if (data.type) {
            // result is not error
            targets.push({...data, periodicity: source.periodicity})
          }
        }

        for (const target of targets) {
          if (target.type === 'newspaper') {
            await this.subscribeNewspaper({
              fullName: target.fullName,
              donation: 0
            })
          }
          if (target.type === 'author') {
            await this.subscribeAuthor({
              author: {id: target.id},
              periodicity: target.periodicity,
              donation: 0
            })
          }
        }

        this.$router.push("/")
      }
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
