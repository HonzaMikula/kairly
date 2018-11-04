<template>
  <div class="follow-author"
    v-if="show"
    v-on-clickaway="() => closeSubscribeWidget()">

    <div v-if="showCanceling === true && cancelingSubscription === true">
      <header>What to do?</header>

      <section>
        <ul>
          <li><a href="" v-on:click.prevent="editSubscription($event)">Edit</a></li>
          <li>
              <a v-if="subscription && subscription.renewal" href="" v-on:click.prevent="cancelSubscription($event)">Cancel subscription</a>
              <a v-else href="" v-on:click.prevent="renewSubscription($event)">Renew subscription</a>
          </li>
        </ul>
      </section>
    </div>

    <div v-else-if="frequency === null">
      <header>How often do you want to read it?</header>

      <section>
        <ul>
          <li><a href="" v-on:click.prevent="selectHowOften('3x_per_day', $event)">3x per day</a></li>
          <li><a href="" v-on:click.prevent="selectHowOften('daily', $event)">Daily</a></li>
          <li><a href="" v-on:click.prevent="selectHowOften('weekly', $event)">Weekly</a></li>
        </ul>
      </section>
    </div>

    <div v-else-if="frequency === 'weekly' && dow === null">
      <header>
        Which day?
        <button-icon role="button" tabindex="0" v-on:click="goOneStepBack()"></button-icon>
      </header>

      <section>
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
    </div>

    <div v-else-if="(frequency === 'weekly' || frequency === 'daily') && time === null">
      <header>
        What time?
        <button-icon role="button" tabindex="0" v-on:click="goOneStepBack()"></button-icon>
      </header>

      <section>
        <ul>
          <li><a href="" v-on:click.prevent="selectWhatTime('6:00', $event)">Early morning (6:00)</a></li>
          <li><a href="" v-on:click.prevent="selectWhatTime('9:00', $event)">Morning (9:00)</a></li>
          <li><a href="" v-on:click.prevent="selectWhatTime('12:00', $event)">Noon (12:00)</a></li>
          <li><a href="" v-on:click.prevent="selectWhatTime('15:00', $event)">After noon (15:00)</a></li>
          <li><a href="" v-on:click.prevent="selectWhatTime('18:00', $event)">Evening (18:00)</a></li>
          <li><a href="" v-on:click.prevent="selectWhatTime('21:00', $event)">Night (21:00)</a></li>
        </ul>
      </section>
    </div>

    <div v-else>
      <header>You're subscribed!</header>

      <section v-if="frequency == '3x_per_day'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> 3x time per day:
        </p>
        <ul class="text">
          <li>Early morning (6:00)</li>
          <li>Noon (12:00)</li>
          <li>Evening (18:00)</li>
        </ul>
      </section>

      <section v-else-if="frequency == 'daily'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> daily at
          <strong>{{ time }}</strong>.
        </p>
      </section>

      <section v-else-if="frequency == 'weekly'">
        <p>
          You will be receiving <strong>{{ author.name }}</strong> weekly on
          <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>.
        </p>
      </section>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

import { directive as onClickaway } from '@/lib/vue-clickaway'

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

  data() {
    return {
      show: false,
      showCanceling: true,
      frequency: null,
      dow: null,
      time: null,
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  methods: {
    ...mapActions(['subscribeAuthor']),
    ...mapMutations(['showError']),

    openSubscribeWidget() {
      this.show = true
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

      if (frequency == '3x_per_day') {
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
    p
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

</style>
