<template>
  <div
    class="change-periodicity-view"
    @click.stop
  >
    <template v-if="frequency === null">
      <header>
        {{ $t('How often do you want to read it?') }}
      </header>

      <section>
        <ul>
          <li><a href="" @click.prevent="selectHowOften('6x_per_day', $event)">{{ $t('Every 3 hours') }}</a></li>
          <li><a href="" @click.prevent="selectHowOften('3x_per_day', $event)">{{ $t('3× per day') }}</a></li>
          <li><a href="" @click.prevent="selectHowOften('daily', $event)">{{ $t('Daily') }}</a></li>
          <li><a href="" @click.prevent="selectHowOften('weekly', $event)">{{ $t('Weekly') }}</a></li>
        </ul>
      </section>
    </template>

    <template v-else-if="frequency === 'weekly' && dow === null">
      <header>
        {{ $t('Which day?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()"></button-icon>
      </header>

      <section>
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
    </template>

    <template v-else-if="(frequency === 'weekly' || frequency === 'daily') && time === null">
      <header>
        {{ $t('What time?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()"></button-icon>
      </header>

      <section>
        <ul>
          <li><a href="" @click.prevent="selectWhatTime('6:00', $event)">{{ $t('Early morning (6:00)') }}</a></li>
          <li><a href="" @click.prevent="selectWhatTime('9:00', $event)">{{ $t('Morning (9:00)') }}</a></li>
          <li><a href="" @click.prevent="selectWhatTime('12:00', $event)">{{ $t('Noon (12:00)') }}</a></li>
          <li><a href="" @click.prevent="selectWhatTime('15:00', $event)">{{ $t('After noon (15:00)') }}</a></li>
          <li><a href="" @click.prevent="selectWhatTime('18:00', $event)">{{ $t('Evening (18:00)') }}</a></li>
          <li><a href="" @click.prevent="selectWhatTime('21:00', $event)">{{ $t('Night (21:00)') }}</a></li>
        </ul>
      </section>
    </template>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'


export default {
  name: 'ChangePeriodicity',

  mixins: [PeriodicityMixin],

  data() {
    return {
      frequency: null,
      dow: null,
      time: null,
    }
  },

  methods: {
    ...mapMutations(['showError']),

    changePeriodicity() {
      this.$emit('changePeriodicity', this.frequency, this.dow, this.time)
    },

    goOneStepBack() {
      if (this.dow !== null) {
        this.dow = null
      } else {
        this.frequency = null
      }
    },

    selectHowOften(frequency, ev) {
      document.activeElement.blur()
      this.frequency = frequency

      if (frequency == '3x_per_day' || frequency == '6x_per_day') {
        this.changePeriodicity()
      }
    },

    selectWhatTime(time, ev) {
      document.activeElement.blur()
      this.time = time
      this.changePeriodicity()
    },

    selectWhatDay(dow, ev) {
      document.activeElement.blur()
      this.dow = dow
    },

    editSubscription(ev) {
      document.activeElement.blur()
      this.frequency = null
    }
  }
}
</script>

<style lang="sass">

.change-periodicity-view
  border-radius: 5px
  margin-bottom: $baseline / 2

  background: #fff
  border: 1px solid lighten($c-base, 30%)
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.15)

  font-family: $ff-sans

  //- header
  header
    position: relative

    padding: 0 $baseline/2

    background: lighten($c-base, 30%)
    color: #000

    font-weight: 600
    font-size: $fs-0
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
    //- menu item
    li
      font-size: $fs-0

      a
        position: relative

        display: block
        padding: 0 $baseline*1.5 0 $baseline/2

        color: #000

        line-height: $baseline * 1.25

        &:first-letter
          text-transform: capitalize

        transition: 0.15s all

        &::after
          +fa-icon()
          @extend .fas
          content: fa-content($fa-var-arrow-right)

          position: absolute
          right: $baseline / 2
          top: 8px

          color: darken($c-base, 20%)
          opacity: 0

          font-size: $fs--1

          transition: 0.15s all

        &:hover
          background: lighten($c-base, 45%)

          &::after
            opacity: 0.5


</style>
