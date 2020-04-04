<template>
  <div class="timeline-time-slot">
    <button
      v-b-tooltip
      :title="$t('Jump to different time')"
      @click="isMenuOpen = !isMenuOpen"
    />

    <h1
      :id="currentAnchor"
      @click="isMenuOpen = !isMenuOpen"
    >
      {{ dayTitle }} – {{ timeTitle }}
    </h1>

    <div
      v-if="isMenuOpen"
      v-on-clickaway="hideJumpMenu"
      class="timeline-navigation--menu"
    >
      <header>
        <h3>{{ $t('Jump to different time') }}</h3>
      </header>

      <section>
        <ul>
          <li v-for="anchor in anchors" :key="anchor.link">
            <a :href="anchor.link" @click="hideJumpMenu">{{ anchor.title }}</a>
          </li>
          <li>
            <a href="#start">{{ $t('Beginning of the day') }}</a>
          </li>
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

  directives: {
    onClickaway
  },

  props: {
    datetime: { type: String, required: true },
    timeSlots: { type: Array, required: true }
  },

  data () {
    return {
      isMenuOpen: false
    }
  },

  computed: {
    dayTitle () {
      const format = this.$i18n.locale === 'cs' ? 'D.M.' : 'M/D'
      const dt = moment(this.datetime)
      const today = moment().format(format)
      const day = dt.format(format)
      const wod = day === today ? this.$t('Today') : dt.format('dddd')
      return `${wod} ${day}`
    },

    timeTitle () {
      return moment(this.datetime).format('H:mm')
    },

    currentAnchor () {
      return `time_${this.timeTitle}`
    },

    anchors () {
      return this.timeSlots.map(slot => {
        const dt = moment(slot.time)
        const h = ~~dt.format('H')
        let title = ''
        // be aware of timezone, in reality time be technically any time
        if (h >= 21) {
          title = this.$t('Night')
        } else if (h >= 18) {
          title = this.$t('Evening')
        } else if (h > 12) {
          title = this.$t('Afternoon')
        } else if (h === 12) {
          title = this.$t('Noon')
        } else if (h >= 9) {
          title = this.$t('Morning')
        } else {
          title = this.$t('Early morning')
        }
        return {
          link: '#time_' + dt.format('H:mm'),
          title: title + ' (' + dt.format('H:mm') + ')'
        }
      })
    }
  },

  methods: {
    hideJumpMenu () {
      this.isMenuOpen = false
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/context-menu'

.timeline-time-slot
  position: relative
  z-index: 2

  display: table
  margin: $baseline*2 auto (-$baseline) auto

  text-align: center

  &:first-of-type
    margin-top: -($baseline * 1.5)

  //- Heading
  > h1
    font-family: $ff-serif
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 1.5
    text-transform: capitalize

    @media (max-width: $mobile)
      font-size: $fs-2

  //- Calendar
  button
    position: absolute
    right: -($baseline * 2)

    display: inline-block
    border-radius: 100%
    height: $baseline * 1.5
    width: $baseline * 1.5

    background: #fafafa
    border: 0
    color: #333

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0

    @media (max-width: $mobile)
      display: none

    &::before
      +fa-icon()
      @extend .fas

      content: fa-content($fa-var-calendar)

    &:focus,
    &:hover
      background: #ddd
      color: #000

.timeline-navigation--menu
  +context-menu

  left: auto
  right: -($baseline * 2 + 105.5px)
  top: $baseline * 2

  @media (max-width: $mobile)
    right: auto
    left: 50%

  li a span
    border-radius: 100%
    display: inline-block
    float: right
    padding: 0 $baseline/4
    margin-top: 6px

    background: #ddd

    line-height: $baseline * 0.8

</style>
