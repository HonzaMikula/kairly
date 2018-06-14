<template>
  <div class="follow-author"
    v-if="show"
    v-on-clickaway="() => closeSubscribeWidget()">

    <section v-if="showCanceling === true && cancelingSubscription === true">
      <header>What to do?</header>
      <ul>
        <li><a href="" v-on:click.prevent="editSubscription($event)">Edit</a></li>
        <li><a href="" v-on:click.prevent="cancelSubscription($event)">Cancel subscription</a></li>
      </ul>
    </section>

    <section v-else-if="period === null">
      <header>How often?</header>
      <ul>
        <li><a href="" v-on:click.prevent="selectHowOften('3x_per_day', $event)">3x per day</a></li>
        <li><a href="" v-on:click.prevent="selectHowOften('daily', $event)">Daily</a></li>
        <li><a href="" v-on:click.prevent="selectHowOften('weekly', $event)">Weekly</a></li>
      </ul>
    </section>

    <section v-else-if="period === 'weekly' && dow === null">
      <header>
        Which day?
        <button-icon tabindex="0" v-on:click="goOneStepBack()"></button-icon>
      </header>
      <ul>
        <li><a href="" v-on:click.prevent="selectWhatDay('1', $event)">Monday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('2', $event)">Tuesday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('3', $event)">Wednesday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('4', $event)">Thursday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('5', $event)">Friday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('6', $event)">Saturday</a></li>
        <li><a href="" v-on:click.prevent="selectWhatDay('7', $event)">Sunday</a></li>
      </ul>
    </section>

    <section v-else-if="(period === 'weekly' || period === 'daily') && time === null">
      <header>
        What time?
        <button-icon tabindex="0" v-on:click="goOneStepBack()"></button-icon>
      </header>
      <ul>
        <li><a href="" v-on:click.prevent="selectWhatTime('6:00', $event)">Early morning (6:00)</a></li>
        <li><a href="" v-on:click.prevent="selectWhatTime('9:00', $event)">Morning (9:00)</a></li>
        <li><a href="" v-on:click.prevent="selectWhatTime('12:00', $event)">Noon (12:00)</a></li>
        <li><a href="" v-on:click.prevent="selectWhatTime('15:00', $event)">After noon (15:00)</a></li>
        <li><a href="" v-on:click.prevent="selectWhatTime('18:00', $event)">Evening (18:00)</a></li>
        <li><a href="" v-on:click.prevent="selectWhatTime('21:00', $event)">Night (21:00)</a></li>
      </ul>
    </section>

    <section v-else>
      <header>You're subscribed!</header>

      <div v-if="period == '3x_per_day'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> 3x time per day:
        </p>
        <ul class="text">
          <li>Early morning (6:00)</li>
          <li>Noon (12:00)</li>
          <li>Evening (18:00)</li>
        </ul>
      </div>

      <div v-else-if="period == 'daily'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> daily at
          <strong>{{ time }}</strong>.
        </p>
      </div>

      <div v-else-if="period == 'weekly'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> weekly on
          <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>.
        </p>
      </div>
    </section>
  </div>
</template>

<script>
import * as api from '@/api'

import { directive as onClickaway } from '@/lib/vue-clickaway'

export default {
  name: 'FollowAuthor',

  props: {
    'author': Object,
    'onSelect': Function,
    'cancelingSubscription': Boolean
  },

  directives: {
    onClickaway
  },

  data() {
    return {
      show: false,
      showCanceling: true,
      period: null,
      dow: null,
      time: null,
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  methods: {
    openSubscribeWidget() {
      this.show = true
    },

    closeSubscribeWidget() {
      this.show = false
      this.period = null
      this.time = null
      this.dow = null
      this.showCanceling = true
    },

    goOneStepBack() {
      if (this.dow !== null) {
        this.dow = null
      } else {
        this.period = null
      }
    },

    submit() {
      this.onSelect(this.period, this.time, this.dow)
    },

    selectHowOften(period, ev) {
      ev.target.blur()
      this.period = period

      if (period == '3x_per_day') {
        this.submit()
      }
    },

    selectWhatTime(time, ev) {
      ev.target.blur()
      this.time = time
      this.submit()
    },

    selectWhatDay(dow, ev) {
      ev.target.blur()
      this.dow = dow
    },

    editSubscription(ev) {
      ev.target.blur()
      this.showCanceling = false
    },

    cancelSubscription() {
      // TODO split handlers
      this.showCanceling = false
      this.$store.dispatch('invalidateTimeline')
      api.unsubscribeAuthor(this.author).then(author => this.author)
      this.author.subscription = null
      ev.target.blur()
    }
  }
}
</script>

<style lang="sass">

.follow-author
  position: absolute
  left: 50%
  top: 50px
  z-index: 1

  margin-left: -125px

  display: block
  border-radius: 5px
  width: 250px

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
      font-size: $fs--2

      &:focus,
      &:hover
        background: lighten($c-base, 15%)
        color: #000

      &::before
        content: $fa-var-arrow-left



  //- steps
  section
    text-align: left

    p
      padding: $baseline / 2

      font-size: $fs--2
      line-height: $baseline * 0.75

      strong
        font-weight: 600

    ul.text
      padding: 0 $baseline/2 $baseline/2 $baseline

      font-size: $fs--2
      line-height: $baseline * 0.75

      li
        list-style: disc

    li a
      position: relative

      display: block
      padding: 0 $baseline/2

      color: #000

      line-height: $baseline * 1.25
      text-decoration: none

      transition: 0.15s all

      &::after
        +fa-icon()

        position: absolute
        right: $baseline / 2
        top: 8px

        color: darken($c-base, 20%)
        opacity: 0

        font-size: $fs--2

        content: $fa-var-arrow-right

        transition: 0.15s all

      &:hover,
      &:focus
        background: lighten($c-base, 40%)

        &::after
          opacity: 1

</style>
