<template>
  <div class="selection-toolbar-view">
    <div class="selection-toolbar--info">
      <span>
        {{ selection.length }} selected posts
      </span>
      <button class="cancel" @click="cleanSelection"></button>
    </div>

    <nav class="selection-toolbar--navigation">
      <button class="up" @click="moveUp()"></button>
      <button class="down" @click="moveDown()"></button>
      <button class="upcoming-issue" id="upcomingIssue" @click="moveUp('upcoming')">Upcoming issue</button>
      <button class="backlog" @click="moveDown('considered')">Backlog</button>
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

  props: {
    newspaper: Object
  },

  computed: {
    selection() {
      return Object.keys(this.$store.state.backlog.selection)
    }
  },

  methods: {
    cleanSelection() {
      this.$store.commit('backlog/cleanSelection')
    },

    moveUp(target=null) {
      const { fullName } = this.newspaper
      const backlogNames = ['upcoming', 'next', 'considered']
      const sources = []
      backlogNames.forEach(name => {
        if (target !== name) {
          const ids = this.$store.state.backlog.newspaperBacklog[fullName][name].layout.map(box => box.id)
          ids.forEach((id, idx) => {
            if (this.selection.indexOf("" + id) !== -1) {
              sources.push({source: name, index: idx})
            }
          })
        }
      })
      // TODO don't move with boxes on top
      sources.forEach(item => {
        this.$store.commit("backlog/moveUp", {
          newspaper: this.newspaper,
          target,
          ...item
        });
      })
    },

    moveDown(target=null) {
      const { fullName } = this.newspaper
      const backlogNames = ['considered', 'next', 'upcoming']
      const sources = []
      backlogNames.forEach(name => {
        if (target !== name) {
          const ids = this.$store.state.backlog.newspaperBacklog[fullName][name].layout.map(box => box.id)
          for (let idx = ids.length - 1; idx >= 0; idx--) {
            const id = ids[idx]
            if (this.selection.indexOf("" + id) !== -1) {
              sources.push({source: name, index: idx})
            }
          }
        }
      })
      // TODO don't move with boxes at bottom
      sources.forEach(item => {
        this.$store.commit("backlog/moveDown", {
          newspaper: this.newspaper,
          target,
          ...item
        });
      })
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
