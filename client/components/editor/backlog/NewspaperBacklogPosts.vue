<template>
  <div class="newspaper-editor-backlog-section" :class="backlog.name">
    <header class="newspaper-editor-backlog--heading">
      <h2>{{ title }}</h2>

      <p>{{ description }}</p>
    </header>

    <div class="newspaper-backlog--next-issue">
      <draggable
        v-model="items"
        group="backlog-posts"
        animation="200"
        handle=".post-content > header"
        :disabled="isTouchDevice"
        @start="drag = true"
        @end="drag = false"
      >
        <transition-group
          type="transition"
          tag="div"
          :name="!drag ? 'flip-list' : null"
        >
          <div
            v-for="(post, idx) in items"
            :key="post.id"
          >
            <NewspaperBacklogPostToolbar
              :index="idx"
              :newspaper="newspaper"
              :backlog="backlog"
            />
            <NewspaperBacklogBox
              :newspaper="newspaper"
              :post="post"
              :can-move-up="idx > 0 || backlog.name !== 'upcoming'"
              :can-move-down="idx < backlog.layout.length - 1 || backlog.name != 'considered'"
              :source="backlog.name"
              :index="idx"
            />
          </div>
        </transition-group>
      </draggable>

      <NewspaperBacklogPostToolbar
        :index="items.length"
        :newspaper="newspaper"
        :backlog="backlog"
        always-visible
      />
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import draggable from 'vuedraggable'

import NewspaperBacklogBox from '@/components/editor/backlog/NewspaperBacklogBox'
import { isTouchDevice } from '@/utils/browser'
import NewspaperBacklogPostToolbar from '@/components/editor/backlog/NewspaperBacklogPostToolbar'

export default {
  name: 'NewspaperBacklogPosts',

  components: {
    draggable,
    NewspaperBacklogBox,
    NewspaperBacklogPostToolbar,
  },

  props: {
    newspaper: { type: Object, required: true },
    title: { type: String, required: true },
    description: { type: String, default: null },
    backlog: { type: Object, required: true },
    posts: { type: Object, required: true }
  },

  data () {
    return {
      drag: false,
      isTouchDevice: false
    }
  },

  computed: {
    items: {
      get () {
        return this.backlog.layout.map((item, idx) => this.getPostObject(item, idx))
      },

      set (value) {
        this.backlogReorder({
          newspaper: this.newspaper,
          target: this.backlog.name,
          ordering: value.filter(p => p).map(p => p.id),
        })
      }
    }
  },

  mounted () {
    this.isTouchDevice = isTouchDevice()
  },

  methods: {
    ...mapActions({
      backlogReorder: 'backlog/reorder'
    }),

    // TODO copied from IssueWrapper
    getPostObject (item, idx) {
      if (item.type === 'post') {
        return this.posts[item.id]
      }
      if (item.type === 'header') {
        return item
      }
      return {
        ...item,
        columns: item.columns.map(c => {
          return {
            css: c.css,
            posts: c.posts.map(item => this.posts[item.id])
          }
        })
      }
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

.flip-list-move
  transition: transform 0.25s

.newspaper-editor-backlog-section
  margin-bottom: $baseline * 2
  max-width: 900px
  padding: 0 $baseline / 2

  background: url('~assets/noise-background.png')

  &.upcoming
    grid-column: 1 / span 2
    grid-row: 1 / span 1
    z-index: 1

    padding-right: $baseline * 2
    box-shadow: 10px 0 5px -5px #ccc

  &.next
    grid-column: 1 / span 2
    grid-row: 2 / span 1
    z-index: 1

    padding-right: $baseline * 2

  &.considered
    grid-column: 2 / span 2
    grid-row: 1 / span 2
    justify-self: flex-end

.newspaper-editor-backlog--heading
  display: grid
  grid-template-columns: $baseline*1.25 1fr auto 1fr $baseline*1.25
  grid-template-rows: auto auto
  grid-column-gap: $baseline / 2
  margin: $baseline 0 $baseline/2 0

  //- heading
  h2
    grid-column: 3

    font-family: $ff-serif
    font-size: $fs-2
    line-height: $baseline * 1.25

  //- when issue will be published
  p
    grid-row: 2
    grid-column: 1 / span 5
    color: #999

    font-family: $ff-serif
    text-align: center

</style>
