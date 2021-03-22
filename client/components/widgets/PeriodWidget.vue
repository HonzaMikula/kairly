<template>
  <div class="period-widget" @click.stop>
    <section v-if="frequency === null">
      <header>{{ $t('How often do you want to publish?') }}</header>
      <ul>
        <li><a href="" @click.prevent="selectHowOften('6x_per_day', $event)">{{ $t('Every 3 hours') }}</a></li>
        <li><a href="" @click.prevent="selectHowOften('3x_per_day', $event)">{{ $t('3x per day') }}</a></li>
        <li><a href="" @click.prevent="selectHowOften('daily', $event)">{{ $t('Daily') }}</a></li>
        <li><a href="" @click.prevent="selectHowOften('weekly', $event)">{{ $t('Weekly') }}</a></li>
      </ul>
    </section>

    <section v-else-if="frequency === 'weekly' && dow === null">
      <header>
        {{ $t('Which day?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()" />
      </header>
      <ul>
        <li><a href="" @click.prevent="selectWhatDay('1', $event)">{{ $t('Monday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('2', $event)">{{ $t('Tuesday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('3', $event)">{{ $t('Wednesday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('4', $event)">{{ $t('Thursday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('5', $event)">{{ $t('Friday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('6', $event)">{{ $t('Saturday') }}</a></li>
        <li><a href="" @click.prevent="selectWhatDay('7', $event)">{{ $t('Sunday') }}</a></li>
      </ul>
    </section>

    <section v-else-if="(frequency === 'weekly' || frequency === 'daily') && time === null">
      <header>
        {{ $t('What time?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()" />
      </header>
      <ul>
        <li><a href="" @click.prevent="selectWhatTime('6:00', $event)">{{ $t('Early morning (6:00)') }}</a></li>
        <li><a href="" @click.prevent="selectWhatTime('9:00', $event)">{{ $t('Morning (9:00)') }}</a></li>
        <li><a href="" @click.prevent="selectWhatTime('12:00', $event)">{{ $t('Noon (12:00)') }}</a></li>
        <li><a href="" @click.prevent="selectWhatTime('15:00', $event)">{{ $t('After noon (15:00)') }}</a></li>
        <li><a href="" @click.prevent="selectWhatTime('18:00', $event)">{{ $t('Evening (18:00)') }}</a></li>
        <li><a href="" @click.prevent="selectWhatTime('21:00', $event)">{{ $t('Night (21:00)') }}</a></li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: 'PeriodWidget',

  data () {
    return {
      frequency: null,
      dow: null,
      time: null,
    }
  },

  methods: {
    goOneStepBack () {
      if (this.dow !== null) {
        this.dow = null
      } else {
        this.frequency = null
      }
    },

    submit () {
      this.$emit('periodicity', this.frequency, this.dow, this.time)
    },

    selectHowOften (frequency, ev) {
      document.activeElement.blur()
      this.frequency = frequency

      if (frequency === '3x_per_day' || frequency === '6x_per_day') {
        this.submit()
      }
    },

    selectWhatTime (time, ev) {
      document.activeElement.blur()
      this.time = time
      this.submit()
    },

    selectWhatDay (dow, ev) {
      document.activeElement.blur()
      this.dow = dow
    }
  }
}
</script>

<style lang="sass">

.period-widget
  position: absolute
  left: 50%
  top: 50px
  z-index: 10005

  margin-left: -125px

  display: block
  border-radius: 5px
  width: 270px

  background: #fff
  border: 1px solid #eee
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.15)

  &::after
    bottom: 100%
    left: 50%
    border: solid transparent
    content: " "
    height: 0
    width: 0
    position: absolute
    pointer-events: none
    border-bottom-color: lighten($c-base, 30%)
    border-width: 15px
    margin-left: -15px

  //- header
  header
    position: relative

    border-radius: 5px 5px 0 0

    background: lighten($c-base, 30%)
    color: #000

    font-weight: 600
    font-size: $fs--1
    line-height: $baseline * 1.25
    text-align: center

    //-- arrow back
    button-icon
      position: absolute
      left: 0

      width: $baseline * 1.25

      color: darken($c-base, 20%)

      cursor: pointer
      font-size: $fs--1

      &:focus,
      &:hover
        background: lighten($c-base, 15%)
        color: #000

      &::before
        content: fa-content($fa-var-arrow-left)

  //- steps
  section
    text-align: left

    p
      padding: $baseline / 2

      font-size: $fs--1
      line-height: $baseline * 0.75

      strong
        font-weight: 600

    ul.text
      padding: 0 $baseline/2 $baseline/2 $baseline

      font-size: $fs--1
      line-height: $baseline * 0.75

      li
        list-style: disc

    li a
      position: relative

      display: block
      padding: 0 $baseline/2

      color: #000

      line-height: $baseline * 1.25

      transition: 0.15s all

      &:first-letter
        text-transform: capitalize

      &::after
        +fa-icon()
        @extend .fas

        position: absolute
        right: $baseline / 2
        top: 8px

        color: darken($c-base, 20%)
        opacity: 0

        font-size: $fs--1

        content: fa-content($fa-var-arrow-right)

        transition: 0.15s all

      &:hover,
      &:focus
        background: lighten($c-base, 40%)

        &::after
          opacity: 1

</style>
