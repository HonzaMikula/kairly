<template>
  <div class="timeline-navigation">
    <button
      @click="showJumpMenu = !showJumpMenu"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      title="Jump to different time"
      :id="currentAnchor"
    >{{ dayTitle }} – {{ timeTitle }}</button>

    <div
      v-if="showJumpMenu"
      v-on-clickaway="() => showJumpMenu = false"
      class="timeline-navigation--menu">
      <header>
        <button-icon tabindex="0"></button-icon>
        <h3>{{ dayTitle }}</h3>
        <button-icon tabindex="0"></button-icon>
      </header>

      <section>
        <ul>
          <li v-for="anchor in anchors">
            <a :href="anchor.link">{{ anchor.title }}</a>
          </li>
          <!--li><a href="">Early morning (6:00)</a></li>
          <li><a href="">Morning (9:00)</a></li>
          <li><a href="">Noon (12:00)</a></li>
          <li><a href="">Afternoon (15:00)</a></li>
          <li><a href="">Evening (18:00)</a></li>
          <li><a href="">Night (21:00)</a></li-->
        </ul>
      </section>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import { directive as onClickaway } from '@/lib/vue-clickaway'

export default {
  name: 'JumpMenu',

  props: {
    datetime: String,
    timeSlots: Array
  },

  directives: {
    onClickaway
  },

  computed: {
    dayTitle() {
      const dt = moment(this.datetime)
      const today = moment().format("M/D");
      const day = dt.format("M/D")
      const wod =  day === today ? 'Today' : dt.format("dddd")
      return `${wod} ${day}`
    },

    timeTitle() {
      return moment(this.datetime).format("H:mm")
    },

    currentAnchor() {
      return `time-slot-${this.timeTitle.replace(':', '-')}`
    },

    anchors() {
      return this.timeSlots.map(slot => {
        const dt = moment(slot.time)
        const h = ~~dt.format("H")
        let title = ''
        // be aware of timezone, in reality time be technically any time
        if (h >= 21) { title = 'Night' }
        else if (h >= 18) { title = 'Evening' }
        else if (h > 12) { title = 'Afternoon' }
        else if (h == 12) { title = 'Noon' }
        else if (h >= 9) { title = 'Morning' }
        else { title = 'Early morning' }
        return {
          link: '#time-slot-' + dt.format("H-mm"),
          title: title + ' (' + dt.format("H:mm") + ')'
        }
      })
    }
  },

  data() {
    return {
      showJumpMenu: false
    }
  },
}
</script>

<style lang="sass">
.timeline-navigation
  position: relative

  margin-bottom: $baseline

  text-align: center

  &::before,
  &::after
    position: absolute

    border-radius: 100%
    height: 7px
    width: 7px

    background: #ddd

    content: ''

  &::before
    margin: 11px 0 0 -30px

  &::after
    margin: 11px 0 0 25px


  button
    display: inline-block
    border-radius: $baseline/2
    height: $baseline
    padding: 0 $baseline/2
    margin-bottom: $baseline /4

    background: #eee
    border: 0

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0


    &:focus,
    &:hover
      background: #ddd

.timeline-navigation--menu
  +context-menu

  li a span
    border-radius: 100%
    display: inline-block
    float: right
    padding: 0 $baseline/4
    margin-top: 6px

    background: #ddd

    line-height: $baseline * 0.8

</style>
