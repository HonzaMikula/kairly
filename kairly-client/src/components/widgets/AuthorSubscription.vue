<template>
  <author-subscription-view>
    <p v-if="period == '3x_per_day'">
      3x time per day: <strong>6:00</strong>, 
      <strong>12:00</strong> and <strong>18:00</strong>.
    </p>

    <p v-else-if="period == 'daily'">
      Daily at <strong>{{ time }}</strong>.
    </p>

    <p v-else-if="period == 'weekly'">
      Weekly on <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>.
    </p>
  </author-subscription-view>
</template>

<script>
export default {
  name: 'AuthorSubscription',
  props: {
    'name': String,
    'subscription': Object
  },

  data() {
    return {
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    period() { return this.subscription && this.subscription.period },
    dow() { return this.subscription && this.subscription.dow },
    time() { return this.subscription && this.subscription.time }
  }
}
</script>

<style lang="sass">
author-subscription-view p
  font-size: $fs--2
</style>
