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
      <button
        id="specialLayout"
        class="special-layout"
        :class="{disabled: !containsOnlyPosts || selection.length < 2 || selection.length > 3}"
        @click.stop
      >Special layout</button>
      <button
        class="delete"
        v-b-tooltip
        :title="$t('Remove post(s)')"
        @click="remove()"
      />

      <b-popover
        target="specialLayout"
        placement="top"
        triggers="click blur"
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
        triggers="click blur"
        @click.stop
      >
        <ul>
          <li tabindex="0" @click="moveToUpcomingTop()">
            <h6>{{ $t('Top') }}</h6>
            <p>{{ $t('Make it first post') }}</p>
          </li>

          <li tabindex="1" @click="moveToUpcomingBottom()">
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
      return Object.keys(this.$store.state.backlog.selection)
    },

    selectedBoxes() {
      const { fullName } = this.newspaper
      const backlogNames = ['upcoming', 'next', 'considered']
      const sources = []
      backlogNames.forEach(name => {
        const { layout } = this.$store.state.backlog.newspaperBacklog[fullName][name]
        layout.forEach((box, index) => {
          if (this.selection.indexOf("" + box.id) !== -1) {
            sources.push({
              source: name,
              index,
              box,
            })
          }
        })
      })
      return sources
    },

    containsOnlyPosts() {
      for (let i = 0; i < this.selectedBoxes.length; i++) {
        if (this.selectedBoxes[i].box.type !== 'post') {
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
      let sources = this.selectedBoxes.slice()
      sources.reverse()
      let selectedBefore = 0
      sources.forEach(item => {
        let index = item.index
        if (item.source === UPPERMOST_BACKLOG) {
          index += selectedBefore
        }
        this.$store.commit("backlog/moveUp", {
          newspaper: this.newspaper,
          source: item.source,
          index,
          target: UPPERMOST_BACKLOG,
          top: true
        })

        selectedBefore++
      })
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveToUpcomingBottom() {
      let sources = this.selectedBoxes
      let selectedBefore = 0
      sources.forEach(item => {
        let index = item.index
        if (item.source === UPPERMOST_BACKLOG) {
          index -= selectedBefore
        }
        this.$store.commit("backlog/moveUp", {
          newspaper: this.newspaper,
          source: item.source,
          index,
          target: UPPERMOST_BACKLOG,
        })

        selectedBefore++
      })
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveUp() {
      let sources = this.selectedBoxes
      let prevSource = null
      let selectedBefore = 0
      sources.forEach(item => {
        if (prevSource !== item.source) {
          prevSource = item.source
          selectedBefore = 0
        }
        let index = item.index - selectedBefore
        if (item.source === UPPERMOST_BACKLOG && index === 0) {
          return
        }

        this.$store.commit("backlog/moveUp", {
          newspaper: this.newspaper,
          source: item.source,
          index,
          target: null
        })
        if (index === 0) {
          selectedBefore++
        }
      })
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveDown(target=null) {
      const { fullName } = this.newspaper
      let sources = this.selectedBoxes.slice()
      sources.reverse()
      if (target) {
        sources = sources.filter(({ source }) => source !== target)
      }

      let consideredSkipIndex = this.$store.state.backlog.newspaperBacklog[fullName][BOTTOMMOST_BACKLOG].layout.length - 1
      sources.forEach(item => {
        if (item.source === BOTTOMMOST_BACKLOG && item.index === consideredSkipIndex) {
          consideredSkipIndex--
          return
        }

        this.$store.commit("backlog/moveDown", {
          newspaper: this.newspaper,
          target,
          source: item.source,
          index: item.index
        })
      })
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    remove() {
      let sources = this.selectedBoxes.slice()
      sources.reverse()
      sources.forEach(item => {
        this.$store.commit("backlog/remove", {
          newspaper: this.newspaper,
          source: item.source,
          index: item.index
        })
      })
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    makeBox(layout, columnsStyle) {
      if (columnsStyle.length !== this.selection.length) {
        return
      }

      let sources = this.selectedBoxes.slice()
      const columns = []
      for (let i = 0; i < sources.length; i++) {
        const { box } = sources[i]
        if (box.type !== 'post') {
          // only posts can be added to box
          return
        }
        columns.push({
          css: columnsStyle[i],
          posts: [box]
        })
      }

      const boxItem = {
        id: Math.random().toString(36).substring(2),
        type: "box",
        css: layout,
        columns
      }

      sources.reverse()
      for (let i = 0; i < sources.length; i++) {
        const item = sources[i]
        if (i === sources.length - 1) {
          // newspaper, target, index, items, deleteCount
          this.$store.commit("backlog/splice", {
            newspaper: this.newspaper,
            target: item.source,
            index: item.index,
            items: [boxItem],
            deleteCount: 1
          })
        } else {
          this.$store.commit("backlog/remove", {
            newspaper: this.newspaper,
            source: item.source,
            index: item.index
          })
        }
      }

      this.cleanSelection()
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
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
