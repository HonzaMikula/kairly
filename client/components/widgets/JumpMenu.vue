<template>
  <div class="timeline-time-slot">
    <button
      @click="isMenuOpen = !isMenuOpen"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :title="$t('Jump to different time')"
      :id="currentAnchor"
    >{{ dayTitle }} – {{ timeTitle }}</button>

    <div
      v-if="isMenuOpen"
      v-on-clickaway="hideJumpMenu"
      class="timeline-navigation--menu">
      <header>
        <h3>{{ $t('Jump to different time') }}</h3>
      </header>

      <section>
        <ul>
          <li v-for="anchor in anchors" :key="anchor.link">
            <a :href="anchor.link" @click="hideJumpMenu">{{ anchor.title }}</a>
          </li>
          <li><a href="#start">{{ $t('Beginning of the day') }}</a></li>
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

  data() {
    return {
      isMenuOpen: false
    }
  },

  computed: {
    dayTitle() {
      const format = this.$i18n.locale === 'cs' ? 'D.M.' : 'M/D'
      const dt = moment(this.datetime)
      const today = moment().format(format);
      const day = dt.format(format)
      const wod =  day === today ? this.$t('Today') : dt.format("dddd")
      return `${wod} ${day}`
    },

    timeTitle() {
      return moment(this.datetime).format("H:mm")
    },

    currentAnchor() {
      return `time_${this.timeTitle}`
    },

    anchors() {
      return this.timeSlots.map(slot => {
        const dt = moment(slot.time)
        const h = ~~dt.format("H")
        let title = ''
        // be aware of timezone, in reality time be technically any time
        if (h >= 21) { title = this.$t('Night') }
        else if (h >= 18) { title = this.$t('Evening') }
        else if (h > 12) { title = this.$t('Afternoon') }
        else if (h == 12) { title = this.$t('Noon') }
        else if (h >= 9) { title = this.$t('Morning') }
        else { title = this.$t('Early morning') }
        return {
          link: '#time_' + dt.format("H:mm"),
          title: title + ' (' + dt.format("H:mm") + ')'
        }
      })
    }
  },

  methods: {
    hideJumpMenu() {
      this.isMenuOpen = false
    }
  }
}
</script>

<style lang="sass">
.timeline-time-slot
  position: relative
  z-index: 2

  display: table
  margin: $baseline*2 auto (-$baseline) auto

  text-align: center

  &:first-of-type
    margin-top: 0

  &::before,
  &::after
    position: absolute

    height: 3px
    width: 50px

    background: #ddd

    content: ''

  &::before
    margin: 11px 0 0 -70px

  &::after
    margin: 11px 0 0 20px


  button
    display: inline-block
    border-radius: $baseline/2
    height: $baseline
    padding: 0 $baseline/2
    margin-bottom: $baseline /4

    background: #eee
    border: 0
    color: #333

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0

    &::before
      +fa-icon()
      @extend .fas

      margin-right: $baseline / 4

      content: fa-content($fa-var-calendar)


    &:focus,
    &:hover
      background: #ddd
      color: #000

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
