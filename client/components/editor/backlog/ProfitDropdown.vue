<template>
  <div class="newspaper-backlog--info--profit-dropdown">

    <table>
      <thead>
        <tr>
          <th>{{ $t('Current Issue') }}</th>
          <th>{{ $t('Per subscriber') }}</th>
          <th>{{ $t('For {subscribers} subscribers', {subscribers: newspaper.likes}) }}</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <th>{{ $t('Avg. revenue per issue') }}</th>
          <td><MoneyFormat :value="revenuePerIssue" currency="Kč" /></td>
          <td><MoneyFormat :value="revenuePerIssue * newspaper.likes" currency="Kč" /></td>
        </tr>
        <tr>
          <th>{{ $t('Cost of current issue') }}</th>
          <td><MoneyFormat :value="currentIssueCost" currency="Kč" /></td>
          <td><MoneyFormat :value="currentIssueCost * newspaper.likes" currency="Kč" /></td>
        </tr>
        <tr class="profit">
          <th>{{ $t('Profit from current issue') }}</th>
          <td><MoneyFormat :value="profitPerIssue" currency="Kč" /></td>
          <td><MoneyFormat :value="profitPerIssue * newspaper.likes" currency="Kč" /></td>
        </tr>
      </tbody>

      <thead>
        <tr>
          <th>{{ $t('Total for this month') }}</th>
          <th>{{ $t('Per subscriber') }}</th>
          <th>{{ $t('For {subscribers} subscribers', {subscribers: newspaper.likes}) }}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>{{ $t('Total revenues') }}</th>
          <td><MoneyFormat :value="newspaper.price" currency="Kč" /></td>
          <td><MoneyFormat :value="newspaper.price * newspaper.likes" currency="Kč" /></td>
        </tr>

        <tr>
          <th>{{ $t('Number of previous issues') }}</th>
          <td colspan="2">{{ currentMonth.priorIssues }}</td>
        </tr>

        <tr>
          <th>{{ $t('Cost of previous issues') }}</th>
          <td><MoneyFormat :value="currentMonth.priorIssuesCost" currency="Kč" /></td>
          <td><MoneyFormat :value="currentMonth.priorIssuesCost * newspaper.likes" currency="Kč" /></td>
        </tr>

        <tr>
          <th>{{ $t('Number of remaining issues') }}</th>
          <td colspan="2">{{ currentMonth.upcomingIssues }}</td>
        </tr>

        <tr class="profit">
          <th>{{ $t('Remaining profit') }}</th>
          <td><MoneyFormat :value="profit" currency="Kč" /></td>
          <td><MoneyFormat :value="profit * newspaper.likes" currency="Kč" /></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import MoneyFormat from '@/components/widgets/MoneyFormat'

export default {
  name: 'ProfitDropdown',

  components: {
    MoneyFormat,
  },

  props: {
    newspaper: Object,
    currentMonth: Object,
    revenuePerIssue: Number,
    currentIssueCost: Number,
    profitPerIssue: Number,
  },

  computed: {
    cost () {
      return parseFloat(this.currentMonth.priorIssuesCost) + this.currentIssueCost
    },

    profit () {
      return parseFloat(this.newspaper.price) - this.cost
    }
  },
}

</script>

<style lang="sass">
//- Detail report dropdown
.newspaper-backlog--info--profit-dropdown
  position: absolute
  right: 0
  top: $baseline
  z-index: 1

  padding: $baseline/4 $baseline/2

  background: #fff
  border: 1px solid #eee
  +box-shadow

  //- general table
  td, th
    padding: $baseline/4 $baseline/2 $baseline/4 0

    font-family: $ff-sans
    text-align: left

  th
    font-weight: 600

  //- header
  thead:last-of-type th
    padding-top: $baseline

  //- body
  tbody th
    font-weight: 400

  tbody td
    text-align: right

    &[colspan]
      text-align: center

      &::before,
      &::after
        content: ' ~ '

  //- profit
  .profit th,
  .profit td
    border-top: 1px solid #555
    font-weight: 600
</style>
