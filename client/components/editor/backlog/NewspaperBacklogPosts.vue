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
        :key="post.id"
        :newspaper="newspaper"
        :post="post"
        :canMoveUp="idx > 0 || backlog.name !== 'upcoming'"
        :canMoveDown="idx < backlog.layout.length - 1 || backlog.name != 'considered'"
        :source="backlog.name"
        :index="idx"
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
            :key="post.id"
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
import { mapActions, mapGetters } from 'vuex'
import draggable from 'vuedraggable'
import keyBy from 'lodash/keyBy'
import isString from 'lodash/isString'

import NewspaperBacklogBox from '@/components/editor/backlog/NewspaperBacklogBox'
import { isTouchDevice } from '@/utils/browser'

export default {
  name: 'NewspaperBacklogPosts',

  components: {
    draggable,
    NewspaperBacklogBox,
  },

  props: {
    newspaper: {type: Object, required: true},
    title: {type: String, required: true},
    description: String,
    backlog: {type: Object, required: true},
    posts: {type: Object, required: true}
  },

  data() {
    return {
      drag: false,
      isTouchDevice: false
    }
  },

  computed: {
    ...mapGetters({
      denormalize: 'entities/denormalize',
    }),

    postsById() {
      return keyBy(this.backlog.posts, 'id')
    },

    items: {
      get() {
        return this.backlog.layout.map((item, idx) => this.getPostObject(item, idx))
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

    // TODO copied from IssueWrapper
    getPostObject(item, idx) {
      if (item.post) {
        return this.denormalize(this.posts[item.post], 'Post')
      }
      if (Array.isArray(item)) {
        const id = Math.random().toString(36).substring(2)
        const css = isString(item[0]) ? item[0] : null
        const columns = css === null ? item : item.slice(1)
        return {
          id,
          type: 'box',
          css,
          columns: columns.map(c => {
            return  {
              css: isString(c[0]) ? c[0] : '',
              posts: (isString(c[0]) ? c.slice(1) : c).map(item => this.denormalize(this.posts[item.post], 'Post'))
            }
          })
        }
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
