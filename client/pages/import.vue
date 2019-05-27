<template>
  <AppLayout :name="$t('Import RSS feeds')">
    <div v-if="sources === null" class="import-rss-empty-view">
      <h1>{{ $t('Import your RSS feeds') }}</h1>

      <p>{{ $t('Export your feeds from your current RSS reader in OPML format and upload the file here.') }}</p>
      <ImportOpmlButton :text="$t('Upload OPML file')" />
    </div>

    <div
      v-else
      class="import-rss-view"
    >
      <h1>{{ $t('RSS feeds to import') }}</h1>

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
                v-on-clickaway="() => closeAllWidgets()"
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
import { Sema } from 'async-sema'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import AppLayout from '@/components/layout/AppLayout'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import ChangePeriodicity from '@/components/widgets/ChangePeriodicity'
import ImportOpmlButton from '@/components/widgets/ImportOpmlButton'

export default {
  name: 'Settings',

  components: {
    AppLayout,
    ChangePeriodicity,
    ImportOpmlButton,
  },

  directives: {
    onClickaway
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

    closeAllWidgets() {
      console.log('ahoj')
      this.showChangePeriodicityDialog.fill(false)
      this.$forceUpdate()
    },

    isKairlyNewspaper(url) {
      return url.match('://kairly\\.com/[^/]+/[^/]+/rss$')
    },

    async submit() {
      const sources = this.sources
        .filter(s => s.selected)
        .map(s => ({url: s.xmlUrl, periodicity: s.periodicity}))

      this.$ga.event({
        eventCategory: 'Onboarding / Exploring',
        eventAction: 'Import RSS feeds',
        eventLabel: null,
        eventValue: sources.length
      })

      if (sources.length) {
        const subscribeData = {
          newspapers: [],
          authors: [],
        }

        this.importing = true
        this.progress = 0
        this.progressTotal = sources.length + 1  // +1 for subscribe

        const s = new Sema(2)

        const importSource = async (source) => {
          await s.acquire()
          try {
            const data = await this.$axios.$post(`/import-rss`, {url: source.url}, { progress: false })
            this.progress += 1

            if (data.type === 'newspaper') {
              subscribeData.newspapers.push({
                fullName: data.fullName
              })
            } else if (data.type === 'author') {
              subscribeData.authors.push({
                username: data.username,
                periodicity: source.periodicity
              })
            }
          } catch (e) {
            console.log(e)
          } finally {
            s.release();
          }
        }

        await Promise.all(sources.map(importSource));

        const { credits } = await this.$axios.$post(`/subscribe-rss`, subscribeData, { progress: false })
        this.progress += 1

        this.$store.commit('updateCredits', credits)
        this.$store.commit('invalidateTimeline')
        this.$store.commit('invalidateSubscriptions')
        this.$router.push("/")
      }
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- Import RSS Empty view
.import-rss-empty-view
  margin: $baseline auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: 0 $baseline / 2

  > h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600
    line-height: 1.42

  > p
    margin-bottom: $baseline

    font-size: $fs-1
    line-height: 1.42

  .import-opml-button
    label
      +button


//- Import RSS
.import-rss-view
  margin: $baseline auto
  max-width: 900px

  @media (max-width: $mobile)
    padding: 0 $baseline / 2

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
    word-break: break-word;

  tbody th
    cursor: pointer

//- Footer
.import-rss--footer
  display: flex
  align-items: center

  @media (max-width: $mobile)
    flex-direction: column

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

    @media (max-width: $mobile)
      margin-right: 0

    &::-webkit-progress-bar
      background: #ddd

    &::-webkit-progress-value,
    &::-moz-progress-bar
      background: $c-base


  // Submit Button
  > button
    +button

    margin-right: $baseline

    @media (max-width: $mobile)
      margin-right: 0
      margin-bottom: $baseline / 2

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
