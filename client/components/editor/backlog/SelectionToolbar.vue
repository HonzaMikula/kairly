<template>
  <div
    class="selection-toolbar-view"

  >
    <div class="selection-toolbar--info">
      <strong>{{ selection.length }}</strong>
      <span>
        selected posts
      </span>
      <button 
        class="cancel" 
        @keydown="cleanSelection"
        tabindex="0"
        @click="cleanSelection"
        v-b-tooltip
        :title="$t('Cancel selection (Escape)')"
      />
    </div>

    <nav class="selection-toolbar--navigation">
      <button 
        class="up" 
        tabindex="0"
        @click="moveUp()" 
      />

      <button 
        class="down"
        @click="moveDown()" 
        tabindex="0"
      />

      <button
        class="upcoming-issue" 
        id="upcomingIssue"
        @click="moveToUpcomingBottom()"
      >
        <span>Upcoming issue</span>
      </button>

      <button 
        class="backlog"
        @click="moveDown('considered')"
      >
        <span>Backlog</span>
      </button>

      <button
        id="specialLayout"
        class="special-layout"
        :class="{disabled: !containsOnlyPosts || selection.length < 2 || selection.length > 3}"
        @click.stop
      >
        <span>Special layout</span>
      </button>

      <button
        class="delete"
        v-b-tooltip
        :title="$t('Remove post(s) (Delete)')"
        @click="remove()"
        @keydown.delete="remove()"
      />

      <b-popover
        target="specialLayout"
        placement="top"
        triggers="hover blur"
        @click.stop
      >
        <ul>
          <li tabindex="0" v-show="selection.length === 2" @click="makeBox('cols-2-1', ['', 'editorial'])">
            <h6>{{ $t('Layout 2-1') }}</h6>
            <p>{{ $t('One main article, one smaller column') }}</p>
          </li>

          <li tabindex="1" v-show="selection.length === 2" @click="makeBox('cols-1-1', ['', ''])">
            <h6>{{ $t('Layout 1-1') }}</h6>
            <p>{{ $t('Two equal sections') }}</p>
          </li>

          <li tabindex="2" v-show="selection.length === 3" @click="makeBox('cols-1-1-1', ['', '', ''])">
            <h6>{{ $t('Layout 1-1-1') }}</h6>
            <p>{{ $t('Three equal sections') }}</p>
          </li>
        </ul>
      </b-popover>

      <b-popover
        target="upcomingIssue"
        placement="top"
        triggers="hover blur"
        @click.stop
      >
        <ul>
          <li tabindex="0" @click="moveToUpcomingTop()">
            <h6>{{ $t('Top') }}</h6>
            <p>{{ $t('Make it first post') }}</p>
          </li>
        </ul>
      </b-popover>
    </nav>

  </div>
</template>

<script>
import { BPopover } from "bootstrap-vue"

const UPPERMOST_BACKLOG = 'upcoming'
const BOTTOMMOST_BACKLOG = 'considered'

export default {
  name: "SelectionToolbar",

  components: {
    BPopover
  },

  props: {
    newspaper: Object
  },

  computed: {
    selection() {
      return this.$store.getters['backlog/getSelection']
    },

    containsOnlyPosts() {
      const selectedBoxes = this.$store.getters['backlog/getSelectedBoxes'](this.newspaper)
      for (let i = 0; i < selectedBoxes.length; i++) {
        if (selectedBoxes[i].box.type !== 'post') {
          return false
        }
      }
      return true
    }
  },

  methods: {
    cleanSelection() {
      this.$store.commit('backlog/cleanSelection')
    },

    moveToUpcomingTop() {
      this.$store.dispatch('backlog/moveToUpcomingTop', {
        newspaper: this.newspaper
      })
    },

    moveToUpcomingBottom() {
      this.$store.dispatch('backlog/moveToUpcomingBottom', {
        newspaper: this.newspaper
      })
    },

    moveUp() {
      this.$store.dispatch('backlog/moveUp', {
        newspaper: this.newspaper
      })
    },

    moveDown(target=null) {
      this.$store.dispatch('backlog/moveDown', {
        newspaper: this.newspaper,
        target
      })
    },

    remove() {
      this.$store.dispatch('backlog/removeBox', {
        newspaper: this.newspaper
      })
    },

    makeBox(layout, columnsStyle) {
      this.$store.dispatch('backlog/makeBox', {
        newspaper: this.newspaper,
        layout,
        columnsStyle
      })
    },
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.selection-toolbar-view
  position: fixed
  bottom: $baseline
  left: 50%
  z-index: 100
  transform: translateX(-50%)

  display: flex
  line-height: $baseline * 1.5
  border-radius: $baseline / 4

  background: #eee
  border: 1px solid #aaa
  box-shadow: 2px 2px 4px #ddd, -2px -2px 4px #fff
  color: #333

  @media (max-width: $mobile)
    bottom: 0
    left: 0

    width: 100%

    border: 0
    border-radius: 0
    border: 1px solid #aaa

    transform: none

//- info panel with how many selected items + cancel
.selection-toolbar--info
  display: flex
  align-items: center
  padding: 0 $baseline / 2
  border-right: 1px solid #aaa

  strong
    margin-right: $baseline / 4

  span
    white-space: nowrap

    @media (max-width: $mobile)
      display: none

  .cancel
    height: $baseline
    margin-left: $baseline / 2
    width: $baseline

    border-radius: 100%
    background: transparent
    border: 0

    cursor: pointer
    text-align: center

    &:hover
      background: #ddd

    &::before
      +fa-icon()
      @extend .fas

      content: fa-content($fa-var-times)


.selection-toolbar--navigation
  display: grid
  flex: 1
  grid-template-columns: repeat(6, min-content)
  grid-template-rows: auto

  @media (max-width: $mobile)
    grid-template-columns: repeat(6, min-content)

  button
    height: $baseline * 1.5
    padding: 0 $baseline/2

    background: transparent
    border: 0

    cursor: pointer
    font-size: $fs-0
    font-family: $ff-sans
    white-space: nowrap
    text-align: center

    @media (max-width: $mobile)
      span
        display: none

      flex: 1

    &:hover,
    &:focus
      background: #ddd

    &::before
      margin-right: $baseline / 4

    &.disabled
      color: #aaa

      &:hover
        background: transparent

  .up
    &::before
      +fa-icon()
      @extend .fas
      margin-right: 0

      content: fa-content($fa-var-arrow-up)

  .down
    &::before
      +fa-icon()
      @extend .fas
      margin-right: 0

      content: fa-content($fa-var-arrow-down)

  .upcoming-issue
    &::before
      +fa-icon()
      @extend .fas

      content: fa-content($fa-var-rocket)    

  .backlog
    &::before
      +fa-icon()
      @extend .fas

      content: fa-content($fa-var-newspaper)

  .special-layout
    &::before
      +fa-icon()
      @extend .fas

      content: fa-content($fa-var-columns)

  .delete
    &::before
      +fa-icon()
      @extend .fas
      margin-right: 0

      content: fa-content($fa-var-trash-alt)


</style>
