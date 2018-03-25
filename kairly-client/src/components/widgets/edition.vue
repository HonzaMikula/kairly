<template>
  <edition-widget>
    <div>
      <h1>When you want to read this edition?</h1>

      <edition-widget--buttons>
        <button 
          v-for="(day, dayIndex) in days" :key="day"
          v-bind:class="{ 'is-active': isDayActive[dayIndex] }"
          v-on:click="setActiveDay(dayIndex)">
          {{ day }}
        </button>
      </edition-widget--buttons>

      <edition-widget--buttons>
        <button 
          v-for="(time, timeIndex) in times" :key="time"
          v-bind:class="{ 'is-active': isTimeActive[timeIndex] }"
          v-on:click="setActiveTime(timeIndex)">
          {{ time }}
        </button>
      </edition-widget--buttons>

      <edition-widget--close-button
        v-on:click="closeEditionMessage()"
        aria-label="Close Dialog">
      </edition-widget--close-button>
    </div>
  </edition-widget>
</template>

<script>

export default {
  name: 'EditionWidget',
  methods: {
    closeEditionMessage: function () {
      this.$emit('editionwidgetclose');
    },

    setActiveDay: function (activeDay) {
      // set all values false
      this.isDayActive.fill(false)

      // set active day
      this.isDayActive[activeDay] = true

      // update component
      this.$forceUpdate()
    },

    setActiveTime: function (activeTime) {
      // set all values false
      this.isTimeActive.fill(false)

      // set active day
      this.isTimeActive[activeTime] = true

      // update component
      this.$forceUpdate()
    }
  },

  data: function() {
    return {
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['Morning', 'Noon', 'Afternoon', 'Evening', 'Night'],
      isDayActive: [false, false, false, false, false, false, false],
      isTimeActive: [false, false, false, false, false]
    }
  }

}
</script>