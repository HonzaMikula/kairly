<template>
  <div class="follow-author"
    v-if="show"
    v-on-clickaway="() => closeSubscribeWidget()">

    <div v-if="showCanceling === true && cancelingSubscription === true">
      <header>{{ $t('What to do?') }}</header>

      <section>
        <ul>
          <li><a href="" @click.stop.prevent="editSubscription($event)">{{ $t('Edit') }}</a></li>
          <li>
              <a v-if="subscription && subscription.state !== 'canceled'" href="" @click.stop.prevent="cancelSubscription($event)">{{ $t('Cancel subscription') }}</a>
              <a v-else href="" @click.stop.prevent="renewSubscription($event)">{{ $t('Renew subscription') }}</a>
          </li>
        </ul>
      </section>
    </div>

    <div v-else-if="frequency === null">
      <header>{{ $t('How often do you want to read it?') }}</header>

      <section>
        <ul>
          <li><a href="" @click.stop.prevent="selectHowOften('6x_per_day', $event)">{{ $t('Immediately') }}</a></li>
          <li><a href="" @click.stop.prevent="selectHowOften('3x_per_day', $event)">{{ $t('3× per day') }}</a></li>
          <li><a href="" @click.stop.prevent="selectHowOften('daily', $event)">{{ $t('Daily') }}</a></li>
          <li><a href="" @click.stop.prevent="selectHowOften('weekly', $event)">{{ $t('Weekly') }}</a></li>
        </ul>
      </section>
    </div>

    <div v-else-if="frequency === 'weekly' && dow === null">
      <header>
        {{ $t('Which day?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()"></button-icon>
      </header>

      <section>
        <ul>
          <li><a href="" @click.stop.prevent="selectWhatDay('1', $event)">{{ $t('Monday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('2', $event)">{{ $t('Tuesday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('3', $event)">{{ $t('Wednesday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('4', $event)">{{ $t('Thursday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('5', $event)">{{ $t('Friday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('6', $event)">{{ $t('Saturday') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatDay('7', $event)">{{ $t('Sunday') }}</a></li>
        </ul>
      </section>
    </div>

    <div v-else-if="(frequency === 'weekly' || frequency === 'daily') && time === null">
      <header>
        {{ $t('What time?') }}
        <button-icon role="button" tabindex="0" @click="goOneStepBack()"></button-icon>
      </header>

      <section>
        <ul>
          <li><a href="" @click.stop.prevent="selectWhatTime('6:00', $event)">{{ $t('Early morning (6:00)') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatTime('9:00', $event)">{{ $t('Morning (9:00)') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatTime('12:00', $event)">{{ $t('Noon (12:00)') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatTime('15:00', $event)">{{ $t('After noon (15:00)') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatTime('18:00', $event)">{{ $t('Evening (18:00)') }}</a></li>
          <li><a href="" @click.stop.prevent="selectWhatTime('21:00', $event)">{{ $t('Night (21:00)') }}</a></li>
        </ul>
      </section>
    </div>

    <div v-else>
      <header>{{ $t('You are subscribed!') }}</header>

      <section v-if="frequency == '6x_per_day'">
        <p v-html="$t('You will be receiving <strong>{authorName}</strong> every 3 hours.', {authorName: author.name})">
        </p>

        <p class="change-button" v-if="!editMode">
          <a href="" @click.stop.prevent="editSubscription($event)">
            {{ $t('Change periodicity and timing') }}
          </a>
        </p>
      </section>

      <section v-else-if="frequency == '3x_per_day'">
        <p v-html="$t('You will be receiving <strong>{authorName}</strong> 3x time per day:', {authorName: author.name})">
        </p>
        <ul class="text">
          <li>{{ $t('Early morning (6:00)') }}</li>
          <li>{{ $t('Noon (12:00)') }}</li>
          <li>{{ $t('Evening (18:00)') }}</li>
        </ul>
      </section>

      <section v-else-if="frequency == 'daily'">
        <p v-html="$t('You will be receiving <strong>{authorName}</strong> daily at <strong>{time}</strong>.', {authorName: author.name, time: time})">
        </p>
      </section>

      <section v-else-if="frequency == 'weekly'">
        <p v-html="$t('You will be receiving <strong>{authorName}</strong> weekly on <strong>{day}</strong> at <strong>{time}</strong>.', {authorName: author.name, day: getDayOfWeekLabel(dow), time: time})">
        </p>
      </section>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

import { directive as onClickaway } from '@/lib/vue-clickaway'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'


export default {
  name: 'FollowAuthor',

  props: {
    author: Object,
    subscription: Object,
    cancelingSubscription: Boolean, // TODO maybe this will be deleted
  },

  directives: {
    onClickaway
  },

  mixins: [PeriodicityMixin],

  data() {
    return {
      show: false,
      showCanceling: true,
      editMode: false,
      frequency: '6x_per_day',
      dow: null,
      time: null,
    }
  },

  methods: {
    ...mapActions(['subscribeAuthor']),
    ...mapMutations(['showError']),

    openSubscribeWidget() {
      this.show = true

      if(!this.subscription) {
        this.submit()
      }
    },

    closeSubscribeWidget() {
      this.show = false
      this.frequency = null
      this.time = null
      this.dow = null
      this.showCanceling = true
    },

    goOneStepBack() {
      if (this.dow !== null) {
        this.dow = null
      } else {
        this.frequency = null
      }
    },

    async submit() {
      console.log([this.author, this.frequency, this.time, this.dow])
      try {
        await this.subscribeAuthor({
          author: this.author,
          periodicity: {
            frequency: this.frequency,
            time: this.time,
            dow: this.dow
          }
        })
      } catch (err) {
        this.showError((err + '') || 'Request failed')
      }
    },

    selectHowOften(frequency, ev) {
      document.activeElement.blur()
      this.frequency = frequency

      if (frequency == '3x_per_day' || frequency == '6x_per_day') {
        this.submit()
      }
    },

    selectWhatTime(time, ev) {
      document.activeElement.blur()
      this.time = time
      this.submit()
    },

    selectWhatDay(dow, ev) {
      document.activeElement.blur()
      this.dow = dow
    },

    editSubscription(ev) {
      document.activeElement.blur()
      this.frequency = null
      this.editMode = true
      this.showCanceling = false
    },

    cancelSubscription() {
      this.showCanceling = false
      this.$store.dispatch('unsubscribeAuthor', {
        author: this.author
      })
      this.closeSubscribeWidget()
    },

    renewSubscription() {
      this.showCanceling = false
      this.$store.dispatch('subscribeAuthor', {
        author: this.author
      })
      this.closeSubscribeWidget()
    }
  }
}
</script>

<style lang="sass">

.follow-author
  +context-menu

  left: 50%
  top: 50px
  z-index: 10000

  margin-left: -135px
  width: 270px

  font-family: $ff-sans

  //- steps
  section
    color: #000

    p
      margin: 0
      padding: $baseline / 2

      font-size: $fs--1
      line-height: $baseline * 0.75

      strong
        font-weight: 600

    ul.text
      padding: 0 $baseline/2 $baseline/2 $baseline
      line-height: $baseline * 0.75

      li
        list-style: disc
        font-size: $fs--1

    li a::after
      content: $fa-var-arrow-right

    //- change button
    .change-button
      margin-top: -($baseline/4)
      margin-bottom: 0
      padding-top: 0

      a
        position: relative

        display: block

        color: $c-base

        &::after
          +fa-icon()

          content: $fa-var-long-arrow-right

          margin-left: $baseline / 4

          opacity: 0

          transition: 0.15s opacity

        &:hover
          color: darken($c-base, 20%)

        &:hover::after
          opacity: 1


</style>
