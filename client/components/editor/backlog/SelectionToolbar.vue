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
      <button class="upcoming-issue" id="upcomingIssue">Upcoming issue</button>
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
          <li tabindex="0" @click="moveUp('upcoming', true)">
            <h6>{{ $t('Top') }}</h6>
            <p>{{ $t('Make it first post') }}</p>
          </li>

          <li tabindex="1" @click="moveUp('upcoming')">
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

    move(target, direction, top=false) {
      const { fullName } = this.newspaper
      const backlogNames = ['upcoming', 'next', 'considered']
      if (direction === 'down' || top) {
        backlogNames.reverse()
      }

      const sources = []
      let canMove = target !== null || top
      backlogNames.forEach(name => {
        if (target !== name || top) {
          const ids = this.$store.state.backlog.newspaperBacklog[fullName][name].layout.map(box => box.id)
          const cb = (id, idx) => {
            if (this.selection.indexOf("" + id) !== -1) {
              if (canMove) {
                sources.push({source: name, index: idx})
              }
            } else {
              canMove = true
            }
          }
          if (direction === 'up' && !top) {
            let movedOut = 0
            for (let idx = 0; idx < ids.length; idx++) {
              // when some post is moved outside section then indexes will be shifted for following items
              const adjustedIdx = idx - movedOut
              cb(ids[idx], adjustedIdx)
              if (adjustedIdx === 0 || target !== null) {
                movedOut++
              }
            }
          } else {
            for (let idx = ids.length - 1; idx >= 0; idx--) {
              cb(ids[idx], idx)
            }
          }
        }
      })

      sources.forEach(item => {
        this.$store.commit(direction === 'up' ? "backlog/moveUp" : "backlog/moveDown", {
          newspaper: this.newspaper,
          target,
          top,
          ...item
        });
      })
    },

    moveUp(target=null, top=false) {
      this.move(target, 'up', top)
    },

    moveDown(target=null) {
      this.move(target, 'down')
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
