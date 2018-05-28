<template>
  <div>
    <div v-if="period == '3X'">
      <p>
        You will be receiving <strong>{{ name }}</strong> 3x time per day:
      </p>
      <ul class="text">
        <li>Early morning (6:00)</li>
        <li>Noon (12:00)</li>
        <li>Evening (18:00)</li>
      </ul>
    </div>

    <div v-else-if="period == 'D'">
      <p>
        You will be receiving <strong>{{ name }}</strong> daily at
        <strong>{{ time }}</strong>.
      </p>
    </div>

    <div v-else-if="period == 'W'">
      <p>
        You will be receiving <strong>{{ name }}</strong> weekly on
        <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>.
      </p>
    </div>
  </div>
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
</style>
