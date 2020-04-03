<template>
  <div class="newspaper-backlog--info">
    <div>
      <p class="newspaper-backlog--info--profit">
        <strong
          v-b-tooltip
          :title="$t('Revenue - Cost = Profit')"
          @click="openProfitDropdown = !openProfitDropdown"
        >
          <MoneyFormat :value="revenuePerIssue" />
          -
          <MoneyFormat :value="currentIssueCost" />
          =
          <MoneyFormat :value="profitPerIssue" currency="Kč" />
        </strong>
      </p>

      <ProfitDropdown
        v-if="openProfitDropdown"
        v-on-clickaway="() => openProfitDropdown = false"
        :newspaper="newspaper"
        :current-month="currentMonth"
        :revenue-per-issue="revenuePerIssue"
        :current-issue-cost="currentIssueCost"
        :profit-per-issue="profitPerIssue"
      />
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import MoneyFormat from '@/components/widgets/MoneyFormat'
import ProfitDropdown from '@/components/editor/backlog/ProfitDropdown'

export default {
  name: 'NewspaperBacklogInfo',

  directives: {
    onClickaway
  },

  components: {
    MoneyFormat,
    ProfitDropdown
  },

  props: {
    newspaper: Object,
    currentMonth: Object,
    // backlogLength: Number,
    published: Array,
  },

  data () {
    return {
      openProfitDropdown: false
    }
  },

  computed: {
    currentIssueCost () {
      return this.published.map(item => item.price).reduce((prev, next) => parseFloat(prev) + parseFloat(next), 0)
    },

    revenuePerIssue () {
      const totalIssues = this.currentMonth.priorIssues + this.currentMonth.upcomingIssues
      return parseFloat(this.newspaper.price) / totalIssues
    },

    profitPerIssue () {
      return this.revenuePerIssue - this.currentIssueCost
    }
  },

  methods: {
    timeFrom (dt) {
      return moment(dt).from()
    },
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- Info when release go out
.newspaper-backlog--info
  display: grid
  grid-template-columns: 970px auto
  grid-column-gap: $baseline

  padding: $baseline/4 0
  margin-bottom: $baseline

  border-bottom: 1px solid #ddd
  border-top: 1px solid #ddd

  font-size: $fs--1
  font-family: $ff-serif
  text-align: center

  > div
    position: relative

    display: flex

    //- report button opening dropdown
    button-icon.report
      &::before
        +fa-icon()
        @extend .fas

        content: fa-content($fa-var-chart-bar)

    p:first-child
      margin-right: auto
</style>
