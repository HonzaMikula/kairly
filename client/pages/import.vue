<template>
  <AppLayout :name="$t('Import')">
    <div v-if="sources === null">
      <WelcomeImportRss style="margin: auto; width: 300px; margin-top: 40px" />
    </div>
    <div
      v-else
      class="import-rss-view"
    >
      <h1>{{ $t('Feeds to import') }}</h1>

      <table>
        <thead>
          <tr>
            <th><input type="checkbox" checked name="" @change="selectAll($event)" /></th>
            <th>{{ $t('Name') }}</th>
            <th>{{ $t('When to display new posts?') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(source, index) in sources" :key="source.xmlUrl">
            <td>
              <input
                v-model="source.selected"
                type="checkbox"
                name=""
              />
            </td>
            <th @click="selectSource(index)">
              {{ source.title }}
            </th>
            <td class="import-rss--change-periodicity">
              <template v-if="isKairlyNewspaper(source.xmlUrl)">
                {{ $t('Subscribe to the newspaper') }}
              </template>
              <template v-else>
                <a href="" @click.prevent.stop="clickChangePeriodicity(source, index)">
                  {{ getPeriodicityLabel(source.periodicity) }}
                </a>
              </template>
              <ChangePeriodicity
                v-if="showChangePeriodicityDialog[index]"
                @changePeriodicity="changePeriodicity"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <footer class="import-rss--footer">
        <button
          @click="submit"
          :disabled="importing"
          :class="{'loading': importing}">
          {{ importing ? $t('Importing feeds') : $t('Import feeds') }}
        </button>
        <template v-if="importing">
          <progress :value="progress" :max="progressTotal"></progress>
          <span>{{ progress }} / {{ progressTotal }}</span>
        </template>
      </footer>
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
      title: this.$t('Import RSS feeds – Kairly')
    }
  },

  data() {
    return {
      importing: false,
      importingTest: false,
      progress: null,
      progressTotal: null,
      showChangePeriodicityDialog: [],
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

    clickChangePeriodicity(source, index) {
      this.changePerodicityTarget = source
      
      if (this.showChangePeriodicityDialog[index]) {
        this.showChangePeriodicityDialog[index] = false
      }
      else {
        this.showChangePeriodicityDialog.fill(false)
        this.showChangePeriodicityDialog[index] = true
      }
    
      this.$forceUpdate()
    },

    selectAll(ev) {
      const value = ev.target.checked
      this.sources.forEach(s => s.selected = value)
      this.$forceUpdate()
    },

    selectSource(index) {
      if (this.sources[index].selected)
        this.sources[index].selected = false
      else
        this.sources[index].selected = true
      this.$forceUpdate()
    },

    changePeriodicity(frequency, dow, time) {
      this.changePerodicityTarget.periodicity = {
        "frequency": frequency,
        "dow": dow,
        "time": time
      }
      this.showChangePeriodicityDialog.fill(false)
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
              donation: 0,
              allowSuspended: true
            })
          }
          if (target.type === 'author') {
            await this.subscribeAuthor({
              author: {id: target.id},
              periodicity: target.periodicity,
              donation: 0,
              allowSuspended: true
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
@import './styles/components/mixins'

//- Import
.import-rss-view
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

  tbody th
    cursor: pointer

//- Footer
.import-rss--footer    
  display: flex
  align-items: center

  // Info label about progress
  > span
    font-size: $fs--1

  // Progress
  progress
    appearance: none
    border: none

    border-radius: $baseline * 1.25/2
    overflow: hidden
    margin-right: $baseline
    height: $baseline / 2
    width: 200px

    background: #ddd

    &::-webkit-progress-bar
      background: #ddd

    &::-webkit-progress-value,
    &::-moz-progress-bar
      background: $c-base



  // Submit Button
  > button
    +button

    margin-right: $baseline

    &.loading::after
      +fa-icon()
      @extend .fas
      +fa-spin

      margin-left: $baseline / 4

      content: fa-content($fa-var-sync)

//- Change periodicity
.import-rss--change-periodicity
  position: relative

  > a
    color: $c-base

    &:focus,
    &:hover
      color: darken($c-base, 10%)

  .change-periodicity-view
    position: absolute
    z-index: 5


</style>
