<template>
  <author-widget v-on:mouseleave="closeWidget()">
    <author-widget--name>{{ author.name }}</author-widget--name>
    <author-widget--medium>{{ author.medium }}</author-widget--medium>
    <img :src="author.picture" :alt="author.name" />  

    <author-widget--stats>
      <div>
      <h3>Editions</h3>
      <p>137</p>
      </div>

      <div>
        <h3>Readers</h3>
        <p>853 478</p>
      </div>

      <div>
        <h3>Articles + Tweets</h3>
        <p>1 203</p>
      </div>
    </author-widget--stats>

    <author-widget--bio>
      {{ author.bio }}
    </author-widget--bio>

    <author-widget--follow>
      <button v-on:click="showPeriods = true" v-bind:class="{'is-active': showPeriods}">{{ showPeriods ? 'Following' : 'Follow' }}</button>

      <author-widget--follow--choose-time v-if="showPeriods">
        <div>
          How often do you want to read?
          <button 
            v-for="(period, periodIndex) in periods" :key="period"
            v-bind:class="{ 'is-active': isPeriodActive[periodIndex] }"
            v-on:click="setActivePeriod(periodIndex)">
            {{ period }}
          </button>
        </div>

 
        <div v-if="showDays">
          Which day do you want to read it?
          <button 
            v-for="(day, dayIndex) in days" :key="day"
            v-bind:class="{ 'is-active': isDayActive[dayIndex] }"
            v-on:click="setActiveDay(dayIndex)">
            {{ day }}
          </button>
        </div>

    

        <div v-if="showDaysInMonth">
          Which day in the month do you want to read it? 
          <button 
            v-for="(dayInMonth, dayInMonthIndex) in daysInMonth" :key="dayInMonth"
            v-bind:class="{ 'is-active': isDayInMonthActive[dayInMonthIndex] }"
            v-on:click="setActiveDayInMonth(dayInMonthIndex)">
            {{ dayInMonth }}
          </button>
        </div>

        <div v-if="showTimes">
          Which day time?
          <button 
            v-for="(time, timeIndex) in times" :key="time"
            v-bind:class="{ 'is-active': isTimeActive[timeIndex] }"
            v-on:click="setActiveTime(timeIndex)">
            {{ time }}
          </button>
        </div>
      </author-widget--follow--choose-time>
    </author-widget--follow>
  </author-widget>
</template>

<script>

export default {
  name: 'cAuthorWidget',
  props: ["author"],
  created: function () {
    // set all 'active' arrays to false
    this.isPeriodActive.fill(false)
    this.isDayActive.fill(false)
    this.isTimeActive.fill(false)
    this.isDayInMonthActive.fill(false)
  },

  methods: {
    closeWidget: function () {
      this.$emit('authorwidgetclose');
    },

    setActivePeriod: function (activePeriod) {
      // set all values false
      this.isPeriodActive.fill(false)
      this.showDaysInMonth = false
      this.showDays = false
      this.showTimes = false

      // set active period
      this.isPeriodActive[activePeriod] = true

      // decide what to show next
      if (activePeriod == 1) { // Daily
        this.showTimes = true
      } else if (activePeriod == 2) { // Weekly
        this.showDays = true
        this.showTimes = true
      } else if (activePeriod == 3) { // Monthly
        this.showDaysInMonth = true
        this.showTimes = true
      }

      // update component
      this.$forceUpdate()
    },

    setActiveDay: function (activeDay) {
      // set all values false
      this.isDayActive.fill(false)

      // set active day
      this.isDayActive[activeDay] = true

      // update component
      this.$forceUpdate()
    },

    setActiveDayInMonth: function (activeDayInMonth) {
      // set all values false
      this.isDayInMonthActive.fill(false)

      // set active day in month
      this.isDayInMonthActive[activeDayInMonth] = true

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
  data: function () {
    return {
      showPeriods: false,
      showDays: false,
      showTimes: false,
      showDaysInMonth: false,
      periods: ['Immediately', 'Daily', 'Weekly', 'Monthly', 'Custom'],
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['Morning', 'Noon', 'Afternoon', 'Evening', 'Night'],
      daysInMonth: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
      isPeriodActive: [],
      isDayActive: [],
      isTimeActive: [],
      isDayInMonthActive: []
    }
  }
}
</script>