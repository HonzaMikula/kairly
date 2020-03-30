<template>
  <div class="selection-toolbar-view">
    <div class="selection-toolbar--info">
      <span>
        {{ selectionSize }} selected posts
      </span>
      <button class="cancel" @click="cleanSelection"></button>
    </div>

    <nav class="selection-toolbar--navigation">
      <button class="up"></button>
      <button class="down"></button>
      <button class="upcoming-issue" id="upcomingIssue">Upcoming issue</button>
      <button class="backlog">Backlog</button>
      <button class="special-layout" id="specialLayout" @click.stop>Special layout</button>
      <button
        class="delete"
        v-b-tooltip
        :title="$t('Remove post(s)')"
      />

      <b-popover
        target="specialLayout"
        placement="top"
        triggers="click blur"
        @click.stop
      >
        <ul>
          <li tabindex="0">
            <h6>{{ $t('Layout 2-1') }}</h6>
            <p>{{ $t('One main article, one smaller column') }}</p>
          </li>

          <li tabindex="1">
            <h6>{{ $t('Layout 1-1') }}</h6>
            <p>{{ $t('Two equal sections') }}</p>
          </li>

          <li tabindex="2">
            <h6>{{ $t('Layout 1-1-1') }}</h6>
            <p>{{ $t('Three equal sections') }}</p>
          </li>
        </ul>
      </b-popover>

      <b-popover
        target="upcomingIssue"
        placement="top"
        triggers="click blur"
        @click.stop
      >
        <ul>
          <li tabindex="0">
            <h6>{{ $t('Top') }}</h6>
            <p>{{ $t('Make it first post') }}</p>
          </li>

          <li tabindex="1">
            <h6>{{ $t('Bottom') }}</h6>
            <p>{{ $t('Make it last post') }}</p>
          </li>
        </ul>
      </b-popover>
    </nav>

  </div>
</template>

<script>
import { BPopover } from "bootstrap-vue"

export default {
  name: "SelectionToolbar",

  components: {
    BPopover
  },

  computed: {
    selectionSize() {
      return Object.keys(this.$store.state.backlog.selection).length
    }
  },

  methods: {
    cleanSelection() {
      this.$store.commit('backlog/cleanSelection')
    }
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

//- info panel with how many selected items + cancel
.selection-toolbar--info
  display: flex
  align-items: center
  padding: 0 $baseline / 2
  border-right: 1px solid #aaa

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
  display: flex

  button
    height: $baseline * 1.5
    padding: 0 $baseline/2

    background: transparent
    border: 0

    cursor: pointer
    font-size: $fs-0
    font-family: $ff-sans

    &:hover,
    &:focus
      background: #ddd

    &::before
      margin-right: $baseline / 4

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
