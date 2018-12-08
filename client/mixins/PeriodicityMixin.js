
export default {
  methods: {
    getDayOfWeekLabel(dow) {
      const $t = this.$t.bind(this)

      const DAYS_OF_WEEK = [
        $t('Monday'), $t('Tuesday'), $t('Wednesday'),
        $t('Thursday'), $t('Friday'), $t('Saturday'), $t('Sunday')
      ]

      return DAYS_OF_WEEK[dow - 1]
    },

    getPeriodicityLabel({ frequency, time, dow }) {
      const $t = this.$t.bind(this)

      if (frequency === '3x_per_day') {
        return $t('Daily at 6:00, 12:00 and 18:00')
      }
      if (frequency === '6x_per_day') {
        return $t('Daily every 3 hours')
      }
      if (frequency === 'daily') {
        return $t('Daily at {at}', {at: time})
      }
      if (frequency === 'weekly') {
        return $t('Every {dow} at {at}', {
          dow: this.getDayOfWeekLabel(dow),
          at: time
        })
      }
    }
  }
}
