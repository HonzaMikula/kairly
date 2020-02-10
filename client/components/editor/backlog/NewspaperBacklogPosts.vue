<template>
  <div class="newspaper-editor-backlog-section">
    <header class="newspaper-editor-backlog--heading">
      <h2>{{ title }}</h2>

      <p>{{ description }}</p>
    </header>


    <div class="newspaper-backlog--next-issue">
      <div v-show="!backlog.layout.length" class="no-post">
        <h2>{{ $t('No posts in backlog') }}</h2>
      </div>

      <NewspaperBacklogBox
        v-for="(post, idx) in items"
        :key="idx"
        :newspaper="newspaper"
        :post="post"
        :canMoveUp="idx > 0 || backlog.name !== 'upcoming'"
        :canMoveDown="idx < backlog.layout.length - 1 || backlog.name != 'considered'"
        :source="backlog.name"
      />

      <!--draggable
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
          <NewspaperBacklogBox
            v-for="(post, idx) in items"
            :key="idx"
            :newspaper="newspaper"
            :post="post"
            :canMoveUp="idx > 0 || backlog.name !== 'upcoming'"
            :canMoveDown="idx < backlog.layout.length - 1 || backlog.name != 'considered'"
            :source="backlog.name"
          />
        </transition-group>
      </draggable-->
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions } from 'vuex'
import draggable from 'vuedraggable'
import keyBy from 'lodash/keyBy'

import NewspaperBacklogBox from '@/components/editor/backlog/NewspaperBacklogBox'
import { isTouchDevice } from '@/utils/browser'

export default {
  name: 'NewspaperBacklogPosts',

  components: {
    draggable,
    NewspaperBacklogBox,
  },

  props: {
    newspaper: Object,
    title: String,
    description: String,
    backlog: Object
  },

  data() {
    return {
      drag: false,
      isTouchDevice: false
    }
  },

  computed: {
    postsById() {
      return keyBy(this.backlog.posts, 'id')
    },

    items: {
      get() {
        return this.backlog.layout.map(item => this.getPostObject(item))
      },

      set(value) {
        this.backlogReorder({
          newspaper: this.newspaper,
          source: this.backlog.name,
          posts: value,
        })
      }
    }
  },

  methods: {
    ...mapActions({
      backlogReorder: 'backlog/reorder'
    }),

    getPostObject(item) {
      if (item.post) {
        return this.postsById[item.post]
      }
      if (Array.isArray(item)) {
        return item.map(i => this.getPostObject(i))
      }
      return item
    }
  },


  mounted() {
    this.isTouchDevice = isTouchDevice()
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

//- Next Issue
.newspaper-backlog--next-issue
  .no-post
    display: flex
    align-items: center
    justify-content: center
    flex-direction: column
    height: 100%
    max-height: 50vh

    color: #999

    &::before
      +fa-icon()
      @extend .fas

      display: block
      margin-bottom: $baseline

      font-size: $fs-4

      content: fa-content($fa-var-clock)

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center
</style>
