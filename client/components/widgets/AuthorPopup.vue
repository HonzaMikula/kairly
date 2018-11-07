<template>
  <author-widget v-on:mouseleave="closeWidget()">
    <author-widget--name>{{ author.name }}</author-widget--name>
    <author-widget--medium>{{ author.medium }}</author-widget--medium>
    <img :src="author.picture" :alt="author.name" />

    <author-widget--stats>
      <div>
      <h3>Newspapers</h3>
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
          <h3>How often do you want to read?</h3>
          <button
            v-for="(period, periodIndex) in periods" :key="period"
            v-bind:class="{ 'is-active': isPeriodActive[periodIndex] }"
            v-on:click="setActivePeriod(periodIndex)">
            {{ period }}
          </button>
        </div>


        <div v-if="showDays">
          <h3>Which day do you want to read it?</h3>
          <button
            v-for="(day, dayIndex) in days" :key="day"
            v-bind:class="{ 'is-active': isDayActive[dayIndex] }"
            v-on:click="setActiveDay(dayIndex)">
            {{ day }}
          </button>
        </div>



        <div v-if="showDaysInMonth">
          <h3>Which day in the month do you want to read it?</h3>
          <button
            v-for="(dayInMonth, dayInMonthIndex) in daysInMonth" :key="dayInMonth"
            v-bind:class="{ 'is-active': isDayInMonthActive[dayInMonthIndex] }"
            v-on:click="setActiveDayInMonth(dayInMonthIndex)">
            {{ dayInMonth }}
          </button>
        </div>

        <div v-if="showTimes">
          <h3>Which day time?</h3>
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
  name: 'AuthorWidget',

  props: {
    author: Object
  },

  created() {
    // set all 'active' arrays to false
    this.isPeriodActive.fill(false)
    this.isDayActive.fill(false)
    this.isTimeActive.fill(false)
    this.isDayInMonthActive.fill(false)
  },

  methods: {
    closeWidget() {
      this.$emit('authorwidgetclose');
    },

    setActivePeriod(activePeriod) {
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

    setActiveDay(activeDay) {
      // set all values false
      this.isDayActive.fill(false)

      // set active day
      this.isDayActive[activeDay] = true

      // update component
      this.$forceUpdate()
    },

    setActiveDayInMonth(activeDayInMonth) {
      // set all values false
      this.isDayInMonthActive.fill(false)

      // set active day in month
      this.isDayInMonthActive[activeDayInMonth] = true

      // update component
      this.$forceUpdate()
    },

    setActiveTime(activeTime) {
      // set all values false
      this.isTimeActive.fill(false)

      // set active day
      this.isTimeActive[activeTime] = true

      // update component
      this.$forceUpdate()
    }
  },

  data() {
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

<style lang="sass">
//- AUTHOR WIDGET -//

author-widget
  position: absolute
  left: $baseline * 2
  top: $baseline * 1.25
  z-index: 1

  display: grid
  grid-template-areas: "author-widget-picture author-widget-name" "author-widget-picture author-widget-medium" "author-widget-picture author-widget-stats" "author-widget-bio author-widget-bio" "author-widget-follow author-widget-follow"
  grid-template-columns: $baseline * 3 auto
  grid-template-rows: $baseline * 0.75 $baseline * 0.75 $baseline * 1.5 auto
  grid-column-gap: $baseline / 2

  border-radius: 5px
  padding: $baseline / 4
  width: 400px

  background: #fff
  border: 1px solid #eee
  box-shadow: 1px 1px 3px #999

  font-size: $fs--1
  line-height: 22px

  //- arrow
  &::after
    position: absolute
    bottom: 100%
    left: 0

    border: solid transparent
    border-color: transparent
    border-bottom-color: #eee
    border-width: 15px

    height: 0
    margin-left: $baseline
    width: 0

    content: ""
    pointer-events: none

  //- Image
  img
    grid-area: author-widget-picture

    border-radius: $baseline / 4
    width: $baseline * 3

//- Name
author-widget--name
  grid-area: author-widget-name

  font-size: $fs--1
  font-weight: 600
  line-height: 18px


//- Medium
author-widget--medium
  grid-area: author-widget-medium
  align-self: center

  color: #555

  font-size: $fs--1
  line-height: 18px


//- Bio
author-widget--bio
  grid-area: author-widget-bio

  margin-top: $baseline / 2

  font-size: $fs--1
  line-height: 1.52

//- Stats
author-widget--stats
  position: relative
  top: 3px

  display: flex
  grid-area: author-widget-stats
  align-self: end

  //- containers
  > div
    margin-right: $baseline

    white-space: nowrap


  //- labels
  h3
    color: #999

    line-height: 18px

  //- values
  p
    font-weight: 600
    font-size: $fs--1
    line-height: 18px


//- Follow button
author-widget--follow
  grid-area: author-widget-follow

  > button
    border-radius: 13px
    height: $baseline
    padding: 0 $baseline

    background: #fff
    border: 1px solid $c-base

    cursor: pointer

    &:focus,
    &:hover,
    &.is-active
      background: $c-base
      border: 1px solid $c-base
      color: #fff



//-- Chose time
author-widget--follow--choose-time
  display: block
  padding-top: $baseline / 2

  > div
    margin-bottom: $baseline / 2

    &:last-of-type
      margin-bottom: 0

  h3
    font-weight: 600

  button
    border-radius: $baseline/4
    padding: 0 $baseline/4


    background: #fff
    border: 0
    color: #000

    cursor: pointer

    &.is-active
      background: $c-base
      color: #fff

      font-weight: 600
</style>
