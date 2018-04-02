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
    closeEditionMessage() {
      this.$emit('editionwidgetclose');
    },

    setActiveDay(activeDay) {
      // set all values false
      this.isDayActive.fill(false)

      // set active day
      this.isDayActive[activeDay] = true

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
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['Morning', 'Noon', 'Afternoon', 'Evening', 'Night'],
      isDayActive: [false, false, false, false, false, false, false],
      isTimeActive: [false, false, false, false, false]
    }
  }

}
</script>

<style lang="sass">
//- EDITION WIDGET -//

edition-widget
  position: absolute
  left: -275px
  top: $baseline * 1.5
  z-index: 1

  margin-left: $baseline * 1.75

  color: #fff

  font-size: $fs--1
  font-weight: 100
  line-height: 20px
  white-space: normal

  //- Arrow
  &::after
    position: absolute
    bottom: 100%
    left: 50%
    
    height: 0
    margin-left: -$baseline / 2
    width: 0
    
    border: solid transparent
    border-bottom-color: transparentize($c-base, 0.05)
    border-width: $baseline / 2
    
    content: " "
    pointer-events: none

  //- Wrapper
  > div
    border-radius: $baseline / 4
    box-sizing: border-box
    padding: $baseline / 2
    width: 480px

    background: transparentize($c-base, 0.1)
    backdrop-filter: blur(5px)

  //- Heading
  h1 
    text-align: center  


//- Buttons wrapper
edition-widget--buttons
  display: block
  margin-top: $baseline / 2

  text-align: center

  //- Buttons
  button
    display: inline-block
    border-radius: $baseline / 2
    height: $baseline
    padding: 0 $baseline / 2
    margin: 0 $baseline / 8

    background: transparent
    border: 1px solid #fff
    color: #fff
    opacity: 0.7

    font-family: $ff-sans
    font-size: $fs--2
    font-weight: 100

    cursor: pointer
    transition: 0.15s opacity

    &:focus,
    &:hover
      opacity: 1

    &.is-active
      background: #fff
      color: #000
      opacity: 1


//- Close Button
edition-widget--close-button
  position: absolute
  right: 0
  top: 0

  height: $baseline
  width: $baseline

  opacity: 0.5

  cursor: pointer
  text-align: center

  transition: 0.15s opacity

  &:focus,
  &:hover
    opacity: 1

  &::after
    +fa-icon()

    content: $fa-var-times    
</style>
