<template>
  <div class="selection-toolbar-view">
    <div class="selection-toolbar--info">
      <strong>{{ selection.length }}</strong>
      <span>
        {{ $t('selected posts') }}
      </span>
      <button
        v-b-tooltip
        class="cancel"
        tabindex="0"
        :title="$t('Cancel selection (ESC)')"
        @click="cleanSelection"
      />
    </div>

    <nav class="selection-toolbar--navigation">
      <button
        v-b-tooltip
        class="up"
        tabindex="0"
        :title="$t('Move up (⬆)')"
        @click="moveUp()"
      />

      <button
        v-b-tooltip
        class="down"
        tabindex="0"
        :title="$t('Move down (⬇)')"
        @click="moveDown()"
      />

      <button
        id="upcomingIssue"
        class="upcoming-issue"
        @click="moveToUpcomingBottom()"
      >
        <span>{{ $t('Upcoming issue') }}</span>
      </button>

      <button
        id="backlog"
        class="backlog"
        @click="moveDown('considered')"
      >
        <span>{{ $t('Backlog') }}</span>
      </button>

      <button
        id="specialLayout"
        class="special-layout"
        :class="{disabled: !containsOnlyPosts || selection.length < 2 || selection.length > 3}"
        @click.stop
      >
        <span>{{ $t('Special layout') }}</span>
      </button>

      <button
        v-b-tooltip
        class="rename"
        :disabled="!isOnlyHeading"
        :title="$t('Rename')"
        @click="renameHeading()"
      />

      <button
        v-b-tooltip
        class="delete"
        :title="$t('Remove post(s) (Del)')"
        @click="remove()"
      />

      <b-popover
        target="specialLayout"
        placement="top"
        triggers="hover blur"
        @click.stop
      >
        <ul>
          <li v-show="selection.length === 2" tabindex="0" @click="makeBox('cols-2-1', ['', 'editorial'])">
            <h6>{{ $t('Layout 2-1') }}</h6>
            <p>{{ $t('One main article, one smaller column') }}</p>
          </li>

          <li v-show="selection.length === 2" tabindex="0" @click="makeBox('cols-1-2', ['', 'editorial'])">
            <h6>{{ $t('Layout 1-2') }}</h6>
            <p>{{ $t('One smaller column, one main article') }}</p>
          </li>

          <li v-show="selection.length === 2" tabindex="1" @click="makeBox('cols-1-1', ['', ''])">
            <h6>{{ $t('Layout 1-1') }}</h6>
            <p>{{ $t('Two equal sections') }}</p>
          </li>

          <li v-show="selection.length === 3" tabindex="2" @click="makeBox('cols-1-1-1', ['', '', ''])">
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
            <p>{{ $t('Make it headline (T)') }}</p>
          </li>
          <li
            v-for="section in upcomingIssueSections"
            :key="section.index"
            @click="pasteSelection('upcoming', section.index)"
          >
            {{ section.title }}
          </li>
          <li tabindex="0" @click="moveToUpcomingBottom()">
            <h6>{{ $t('Bottom') }}</h6>
            <p>{{ $t('Append to the issue (G)') }}</p>
          </li>
        </ul>
      </b-popover>

      <b-popover
        v-if="backlogSections.length > 0"
        target="backlog"
        placement="top"
        triggers="hover blur"
        @click.stop
      >
        <ul>
          <li>
            <h6>{{ $t('Move to backlog') }}</h6>
            <p>{{ $t('Keyboard shortcut (X)') }}</p>
          </li>
          <li
            v-for="section in backlogSections"
            :key="section.index"
            @click="pasteSelection('considered', section.index)"
          >
            {{ section.title }}
          </li>
        </ul>
      </b-popover>
    </nav>
  </div>
</template>

<script>
import { BPopover } from 'bootstrap-vue'
import PostObjectMixin from '@/mixins/PostObjectMixin'

export default {
  name: 'SelectionToolbar',

  components: {
    BPopover
  },

  mixins: [PostObjectMixin],

  props: {
    newspaper: { type: Object, required: true }
  },

  computed: {
    selection () {
      return this.$store.getters['backlog/getSelection']
    },

    containsOnlyPosts () {
      const selectedBoxes = this.$store.getters['backlog/getSelectedBoxes'](this.newspaper)
      for (let i = 0; i < selectedBoxes.length; i++) {
        if (selectedBoxes[i].box.type !== 'post') {
          return false
        }
      }
      return true
    },

    isOnlyHeading () {
      const selectedBoxes = this.$store.getters['backlog/getSelectedBoxes'](this.newspaper)
      if (selectedBoxes.length > 1) {
        return false
      }
      if (selectedBoxes[0] && selectedBoxes[0].box && selectedBoxes[0].box.type === 'header') {
        return true
      }
      return false
    },

    backlogSections () {
      const posts = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName].considered.layout
      const sections = []
      posts.forEach((item, index) => {
        if (item.type === 'header') {
          sections.push({ title: item.title, index })
        }
      })
      return sections
    },

    upcomingIssueSections () {
      const posts = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName].upcoming.layout
      const sections = []
      posts.forEach((item, index) => {
        if (item.type === 'header') {
          sections.push({ title: item.title, index })
        }
      })
      return sections
    },
  },

  methods: {
    cleanSelection () {
      this.$store.commit('backlog/cleanSelection')
    },

    moveToUpcomingTop () {
      this.$store.dispatch('backlog/moveSelectionToUpcomingTop', {
        newspaper: this.newspaper
      })
    },

    moveToUpcomingBottom () {
      this.$store.dispatch('backlog/moveSelectionToUpcomingBottom', {
        newspaper: this.newspaper
      })
    },

    moveUp () {
      this.$store.dispatch('backlog/moveSelectionUp', {
        newspaper: this.newspaper
      })
    },

    moveDown (target = null) {
      this.$store.dispatch('backlog/moveSelectionDown', {
        newspaper: this.newspaper,
        target
      })
    },

    remove () {
      const selectedBoxes = this.$store.getters['backlog/getSelectedBoxes'](this.newspaper)
      let proceed = true
      // console.log(selectedBoxes)
      if (selectedBoxes.length > 1) {
        let text = 'You\'re going to delete following posts:\n'
        const posts = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName].$posts

        selectedBoxes.forEach((item) => {
          if (item.box.title) {
            text += `• ${item.box.title} \n`
          } else if (item.box.type === 'post') {
            const title = posts[item.box.id].content.title ? posts[item.box.id].content.title : posts[item.box.id].content.content.slice(0, 100)
            text += `• ${title} \n`
          } else {
            item.box.columns.forEach((column) => {
              if (column.posts.length > 0) {
                column.posts.forEach((post) => {
                  if (posts[post.id]) {
                    let title

                    if (posts[post.id] && posts[post.id].content.title) {
                      title = posts[post.id].content.title
                    } else if (posts[post.id] && posts[post.id].content) {
                      title = posts[post.id].content.content.slice(0, 100)
                    }
                    text += `• ${title} \n`
                  }
                })
              }
            })
          }
        })
        proceed = window.confirm(text)
      }

      if (proceed) {
        this.$store.dispatch('backlog/removeSelectedBox', {
          newspaper: this.newspaper
        })
      }
    },

    makeBox (layout, columnsStyle) {
      this.$store.dispatch('backlog/makeBoxFromSelection', {
        newspaper: this.newspaper,
        layout,
        columnsStyle
      })
    },

    pasteSelection (target, index) {
      const newspaper = this.newspaper
      this.$store.dispatch('backlog/pasteSelection', {
        newspaper,
        target,
        index: index + 1
      })
      this.$store.dispatch('backlog/save', { newspaper })
    },

    renameHeading () {
      const title = window.prompt('Title')
      if (title === null) {
        return
      }
      const newspaper = this.newspaper
      this.$store.dispatch('backlog/updateHeading', { newspaper, title })
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

  background: rgba(255, 255, 255, 0.7)
  backdrop-filter: blur(10px)

  @supports not (backdrop-filter: blur(10px))
    background: #fff

  border: 1px solid rgba(170, 170, 170, 0.5)
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff
  color: #333

  @media (max-width: $mobile)
    bottom: 0
    left: 0

    width: 100%

    border: 0
    border-radius: 0
    border-top: 1px solid rgba(200, 200, 200, 0.5)
    box-shadow: none

    transform: none

//- info panel with how many selected items + cancel
.selection-toolbar--info
  display: flex
  align-items: center
  padding: 0 $baseline / 2
  border-right: 1px solid rgba(200, 200, 200, 0.5)

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
  grid-template-columns: repeat(7, min-content)
  grid-template-rows: auto

  @media (max-width: $mobile)
    grid-template-columns: repeat(7, min-content)

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

  .rename
    &::before
      +fa-icon()
      @extend .fas
      margin-right: 0

      content: fa-content($fa-var-edit)

  .delete
    &::before
      +fa-icon()
      @extend .fas
      margin-right: 0

      content: fa-content($fa-var-trash-alt)

</style>
