<template>
  <compotent
    :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    :typeOverride="typeOverride"
    @click.native="toggleMobileControls"
    @close-editor="closeEditor"
  >
    <template #page-controls="{ post, postIndex, column, columnIndex}">
      <span v-if="post.type === 'newspaper'" class="price">{{ post.price }} Kč</span>
      <template v-else>&nbsp;</template>

      <button-icon
        v-if="post.draft"
        class="edit"
        role="button"
        :title="$t('Edit comment')"
        @click="editComment(post.id)"
      />

      <template v-if="column">
        <button-icon
          v-if="postIndex > 0"
          class="up"
          v-b-tooltip
          tabindex="0"
          role="button"
          :title="$t('Move tweet up')"
          @click="moveUpInColumn(columnIndex, postIndex)"
        />
        <button-icon
          v-if="postIndex < column.posts.length - 1"
          class="down"
          v-b-tooltip
          tabindex="0"
          role="button"
          :title="$t('Move tweet down')"
          @click="moveDownInColumn(columnIndex, postIndex)"
        />
        <button-icon
          class="level-up"
          v-b-tooltip
          tabindex="0"
          role="button"
          :title="$t('Remove from column')"
          @click="removeFromColumn({ post, source, index: index + 1 })"
        />
      </template>
    </template>

    <template #aside>
      <div
        :class="{'newspaper-backlog-controls': true, 'hide-mobile-controls': mobileControls}"
      >
        <div class="newspaper-backlog-controls--arrows">
          <button
            class="up"
            :id="`backlog-controls-up-${post.id}`"
            @click.stop="moveUp()"
            :disabled="!canMoveUp"
          ></button>

          <button
            class="down"
            :id="`backlog-controls-down-${post.id}`"
            @click.stop="moveDown()"
            :disabled="!canMoveDown"
          ></button>

          <button
            class="remove"
            @click.stop="removePost()"
            v-b-tooltip
            title="Remove post"
          ></button>

          <b-popover
            v-if="source !== 'upcoming'"
            :target="`backlog-controls-up-${post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source !== 'upcoming'"
                tabindex="0"
                @click="moveUp('upcoming')"
              >
                <h6>{{ $t('Move to upcoming issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source === 'considered'"
                @click="moveUp('next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>

          <b-popover
            v-if="source !== 'considered'"
            :target="`backlog-controls-down-${post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source === 'upcoming'"
                tabindex="0"
                @click="moveDown('next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source !== 'considered'"
                @click="moveDown('considered')"
              >
                <h6>{{ $t('Move to backlog issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>
        </div>

        <div class="newspaper-backlog-controls--options">
          <template v-if="post.type !== 'box'">
            <button
              class="change-layout"
              :id="`change-layout-${post.id}`"
              @click.stop
            />

            <b-popover
              :target="`change-layout-${post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li
                  tabindex="0"
                  @click="makeBox('cols-2-1', ['', 'editorial'])"
                >
                  <h6>{{ $t('Layout 2-1') }}</h6>
                  <p>{{ $t('Move posts to the column') }}</p>
                </li>

                <li
                  tabindex="1"
                  @click="makeBox('cols-1-1', ['', ''])"
                >
                  <h6>{{ $t('Layout 1-1') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>

                <li
                  tabindex="2"
                  @click="makeBox('cols-1-1-1', ['', '', ''])"
                >
                  <h6>{{ $t('Layout 1-1-1') }}</h6>
                  <p>{{ $t('Change column background') }}</p>
                </li>
              </ul>
            </b-popover>
          </template>
          <template v-else>
            <button
              class="change-position"
              @click="reverseColumns"
              v-b-tooltip
              :title="$t('Change position')"
            />

            <div class="newspaper-backlog-controls--options--columns">
              <template
                v-for="(icon, colIndex) in columnIcons"
              >
                <button
                  :class="icon"
                  :id="`backlog-controls-option-${post.id}-${colIndex}`"
                  v-b-tooltip
                  :title="$t('Column') + ' ' + (colIndex + 1)"
                  @click.stop
                  :key="`btn-${colIndex}`"
                />

                <b-popover
                  :target="`backlog-controls-option-${post.id}-${colIndex}`"
                  placement="bottomleft"
                  triggers="click blur"
                  :key="`btn-popover-${colIndex}`"
                  @click.stop
                >
                  <ul>
                    <li
                      tabindex="0"
                      @click="openPostSelection(colIndex)"
                    >
                      <h6>{{ $t('Select posts') }}</h6>
                      <p>{{ $t('Move posts to the column') }}</p>
                    </li>

                    <li
                      tabindex="1"
                      @click="writeComment(colIndex)"
                    >
                      <h6>{{ $t('Add comment') }}</h6>
                      <p>{{ $t('Write short comment to the topic') }}</p>
                    </li>

                    <li
                      tabindex="2"
                      @click="toggleEditorialStyle(colIndex)"
                    >
                      <h6>{{ $t('Toggle editorlal style') }}</h6>
                      <p>{{ $t('Change column background') }}</p>
                    </li>
                  </ul>
                </b-popover>
              </template>
            </div>

            <button
              class="split-columns"
              @click="splitColumns"
              v-b-tooltip
              :title="$t('Split columns')"
            />
          </template>
        </div>
      </div>

      <portal to="modal">
        <PostsSelection
          v-if="editedColumn !== null"
          :newspaper="newspaper"
          :selected="post.columns[editedColumn].posts.map(p => p.id)"
          @add="addToColumn"
          @remove="removeFromColumn"
          @done="closePostSelection"
        />
      </portal>
    </template>
  </compotent>
</template>

<script>
import Vue from 'vue'
import { mapActions  } from 'vuex'
import { BPopover } from 'bootstrap-vue'

import PostWrapper from '@/components/PostWrapper'
import BoxWrapper from '@/components/BoxWrapper'
import CommentEditor from '@/components/editor/backlog/CommentEditor'
import PostsSelection from '@/components/editor/backlog/PostsSelection'

export default {
  name: 'NewspaperBacklogBox',

  components: {
    PostWrapper,
    BoxWrapper,
    BPopover,
    CommentEditor,
    PostsSelection,
  },

  props: {
    newspaper: Object,
    post: Object,
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: String,
    index: Number
  },

  data() {
    return {
      mobileControls: false,
      editedColumn: null,
      typeOverride: {}
    }
  },

  computed: {
    columnIcons() {
      if (this.post.type !== 'box') {
        return []
      }
      if (this.post.css === 'cols-1-1-1') {
        return ['menu-left-col', 'menu-middle-col', 'menu-right-col']
      }
      return ['menu-left-col', 'menu-right-col']
    },

    isAdmin() {
      const { user } = this.$store.state.auth
      return user.isAdmin
    }
  },

  methods: {
    toggleMobileControls() {
      this.mobileControls = !this.mobileControls
    },

    addToColumn({ post, source, columnIndex=null }) {
      const columns = [...this.post.columns]
      if (columnIndex === null) {
        columnIndex = this.editedColumn
      }
      columns[columnIndex].posts.push({id: post.id, type: 'post'})
      this.setBacklogItem({
        ...this.post,
        columns
      })
      if (source) {
        this.$store.commit('backlog/remove', {
          newspaper: this.newspaper,
          source,
          postId: post.id
        })
      }
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    removeFromColumn({ post, source, index=0 }) {
      const columns = []
      this.post.columns.forEach(col => {
        columns.push({
          ...col,
          posts: col.posts.filter(p => p.id !== post.id)
        })
      })
      this.setBacklogItem({
        ...this.post,
        columns
      })
      this.$store.commit('backlog/splice', {
        newspaper: this.newspaper,
        target: source,
        items: [{id: post.id, type: 'post'}],
        index,
        deleteCount: 0
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    editComment(postId) {
      Vue.set(this.typeOverride, postId, CommentEditor)
    },

    closeEditor(postId) {
      Vue.delete(this.typeOverride, postId)
    },

    moveUpInColumn(columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({id: p.id, type: 'post'}))
        }
        if (idx === columnIndex) {
          const post = col.posts[postIndex]
          col.posts[postIndex] = col.posts[postIndex - 1]
          col.posts[postIndex - 1] = post
        }
        return col
      })
      this.setBacklogItem({
        ...this.post,
        columns
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    moveDownInColumn(columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({id: p.id, type: 'post'}))
        }
        if (idx === columnIndex) {
          const post = col.posts[postIndex]
          col.posts[postIndex] = col.posts[postIndex + 1]
          col.posts[postIndex + 1] = post
        }
        return col
      })
      this.setBacklogItem({
        ...this.post,
        columns
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    openPostSelection(idx=null) {
      this.$root.$emit('post-selection-open', this.post.id)
      if (idx === null) {
        idx = this.post.columns.findIndex(c => c.css === 'editorial')
      }
      this.editedColumn = idx
    },

    closePostSelection() {
      this.editedColumn = null
    },

    async writeComment(idx) {
      const data = {
        type: 'comment',
        title: '',
        content: ''
      }
      const { post } = await this.$axios.$post(`/drafts`, data)
      this.$store.commit('backlog/registerPost', { newspaper: this.newspaper, post })
      this.addToColumn({ post, columnIndex: idx })
      this.editComment(post.id)
    },

    toggleEditorialStyle(columnIdx) {
      this.setBacklogItem({
        ...this.post,
        columns: this.post.columns.map((col, idx) => {
          return {
            ...col,
            css: columnIdx === idx
              ? (col.css === 'editorial' ? '' : 'editorial')
              : col.css
          }
        })
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    moveUp(target=null) {
      this.$store.commit('backlog/moveUp', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    moveDown(target=null) {
      this.$store.commit('backlog/moveDown', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    removePost() {
      this.$store.commit('backlog/remove', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    setBacklogItem(item) {
      this.$store.commit('backlog/setBacklogItem', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        item
      })
    },

    makeBox(layout, columnsStyle) {
      this.setBacklogItem({
        //id: this.post.id, // keep same id to keep same NewspaperBacklogBox, NOT GOOD idea as long as post can be removed
        id: Math.random().toString(36).substring(2),
        type: 'box',
        css: layout,
        columns: columnsStyle.map((css, idx) => {
          return {
            css,
            posts: idx === 0 ? [{id: this.post.id, type: 'post'}] : []
          }
        })
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    splitColumns() {
      this.closePostSelection()
      const posts = []
      this.post.columns.forEach(col => col.posts.forEach(p => posts.push({id: p.id, type: 'post'})))
      this.$store.commit('backlog/splice', {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        items: posts,
        deleteCount: 1
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    reverseColumns() {
      const columns = [...this.post.columns]
      columns.reverse()
      let css = null
      if (this.post.css === 'cols-2-1') {
        css = 'cols-1-2'
      } else if (this.post.css === 'cols-1-2') {
        css = 'cols-2-1'
      } else {
        css = this.post.css
      }
      this.setBacklogItem({ ...this.post, css, columns })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    }
  },

  mounted() {
    this._onSelectionOpen = postId => {
      if (this.post.id !== postId) {
        this.closePostSelection()
      }
    }
    this.$root.$on('post-selection-open', this._onSelectionOpen)
  },

  beforeDestroy() {
    this.$root.$off('post-selection-open', this._onSelectionOpen)
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'


//- Backlog controls
.newspaper-backlog-controls.hide-mobile-controls
  @media (max-width: $mobile)
    display: none

.newspaper-backlog-controls--arrows
  position: absolute
  left: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-row: auto auto
  grid-row-gap: $baseline / 4

  @media (max-width: $mobile)
    left: $baseline/4
    top: 40%

  //- button up
  .up
    +button-icon($fa-var-arrow-up)

  //- button down
  .down
    +button-icon($fa-var-arrow-down)

  //- button down
  .remove
    +button-icon($fa-var-times)

.newspaper-backlog-controls--options
  position: absolute
  right: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-row: auto auto
  grid-row-gap: $baseline / 4
  width: $baseline * 1.25

  @media (max-width: $mobile)
    right: $baseline/4
    top: 40%

  //- button add editorial
  .change-layout
    +button-icon($fa-var-columns)

  //- button add comment
  .edit-comment
    +button-icon($fa-var-pencil-alt)

  //- button menu
  .menu-left-col
    +button-icon($fa-var-align-left)

  .menu-middle-col
    +button-icon($fa-var-align-center)

  .menu-right-col
    +button-icon($fa-var-align-right)

  //- change position button
  .change-position
    +button-icon($fa-var-exchange-alt)

  .split-columns
    +button-icon($fa-var-undo)

//- icons for columns
.newspaper-backlog-controls--options--columns
  white-space: nowrap

  > button
    margin-right: $baseline / 8

.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
