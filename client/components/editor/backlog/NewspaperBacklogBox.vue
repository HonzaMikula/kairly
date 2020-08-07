<template>
  <compotent
    :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    :selected="selected"
    :type-override="typeOverride"
    @close-editor="closeEditor"
    @click.native.stop="selectBox()"
  >
    <template #empty-box="{ columnIndex }">
      <EmptyColumnPlaceholder>
        <button
          v-b-tooltip
          class="add-posts"
          :class="{'is-active': isPostSelectionOpened}"
          :title="$t('Posts')"
          @click="openPostSelection(columnIndex)"
        />

        <button
          v-b-tooltip
          class="add-comment"
          :title="$t('Comment')"
          @click="writeComment(columnIndex)"
        />

        <button
          v-b-tooltip
          class="add-external"
          :title="$t('External post')"
          @click="addExternalLink(columnIndex)"
        />

        <button
          v-b-tooltip
          class="toggle-editorial"
          :title="$t('Toggle editorial')"
          @click="toggleEditorialStyle(columnIndex)"
        />
      </EmptyColumnPlaceholder>
    </template>

    <template #page-controls="{ post, postIndex, column, columnIndex}">
      <span v-if="post.type === 'newspaper'" class="price">{{ post.price }} Kč</span>
      <template v-else>&nbsp;</template>

      <button
        v-if="post.draft"
        v-b-tooltip
        class="edit"
        :title="$t('Edit comment')"
        @click="editComment(post.id)"
      />

      <button
        :id="`post-options-${post.id}`"
        v-b-tooltip
        class="post-options"
        :title="$t('Post options')"
      />

      <b-popover
        :target="`post-options-${post.id}`"
        placement="bottomleft"
        triggers="click hover blur"
        @click.stop
      >
        <ul>
          <template v-if="!columnIcons.length">
            <li v-if="canMoveUp" class="icon-up" tabindex="0" @click="moveUp()">
              <h6>{{ $t('Move up') }}</h6>
            </li>

            <li v-if="canMoveDown" class="icon-down" tabindex="0" @click="moveDown()">
              <h6>{{ $t('Move down') }}</h6>
            </li>

            <template v-if="post.type !== 'box' && post.type !== 'header'">
              <li class="icon-remove" tabindex="0" @click="removePost()">
                <h6>{{ $t('Remove') }}</h6>
              </li>

              <li class="multiple-options">
                <h6>{{ $t('Change layout') }}</h6>
                <div>
                  <button @click="makeBox('cols-1-2', ['editorial', ''])">1-2</button>
                  <button @click="makeBox('cols-2-1', ['', 'editorial'])">2-1</button>
                  <button @click="makeBox('cols-1-1', ['', ''])">1-1</button>
                  <button @click="makeBox('cols-1-1-1', ['', '', ''])">1-1-1</button>
                </div>
              </li>
            </template>
          </template>

          <template v-if="columnIcons.length">
            <li
              v-if="postIndex > 0"
              class="icon-up"
              tabindex="0"
              @click="moveUpInColumn(columnIndex, postIndex)"
            >
              <h6>{{ $t('Move up') }}</h6>
            </li>

            <li
              v-if="postIndex < column.posts.length - 1"
              class="icon-down"
              tabindex="0"
              @click="moveDownInColumn(columnIndex, postIndex)"
            >
              <h6>{{ $t('Move down') }}</h6>
            </li>

            <li
              class="icon-cancel"
              @click="removeFromColumn({ post, source, index: index + 1 })"
            >
              <h6>{{ $t('Remove from column') }}</h6>
            </li>
          </template>
        </ul>
      </b-popover>
    </template>

    <template #aside>
      <div v-if="post.type === 'box' || post.type === 'header'" class="newspaper-backlog-controls">
        <template>
          <button
            :id="`block-controls-${post.id}`"
            v-b-tooltip
            class="block-controls"
            :title="$t('Options')"
            @click.stop
          />

          <b-popover
            :target="`block-controls-${post.id}`"
            placement="bottomleft"
            triggers="click hover blur"
            @click.stop
          >
            <ul>
              <li v-if="canMoveUp" class="icon-up" tabindex="0" @click="moveUp()">
                <h6>{{ $t('Move up') }}</h6>
              </li>

              <li v-if="canMoveDown" class="icon-down" tabindex="0" @click="moveDown()">
                <h6>{{ $t('Move down') }}</h6>
              </li>

              <template v-if="post.type === 'box'">
                <li class="icon-swap" tabindex="0" @click="reverseColumns">
                  <h6>{{ $t('Swap columns') }}</h6>
                </li>

                <li class="icon-cancel" tabindex="0" @click="splitColumns">
                  <h6>{{ $t('Cancel special layout') }}</h6>
                </li>

                <li class="multiple-options">
                  <h6>{{ $t('Toggle editorial') }}</h6>
                  <div>
                    <button
                      v-for="(column, colIndex) in columnIcons"
                      :key="`btn-${colIndex}`"
                      @click="toggleEditorialStyle(colIndex)"
                    >
                      {{ $t('Column') }} {{ colIndex + 1 }}
                    </button>
                  </div>
                </li>
              </template>

              <template v-else-if="post.type === 'header'">
                <li class="icon-edit" tabindex="0" @click="renameHeading()">
                  <h6>{{ $t('Rename') }}</h6>
                </li>

                <li class="icon-remove" tabindex="0" @click="removePost()">
                  <h6>{{ $t('Remove') }}</h6>
                </li>
              </template>
            </ul>
          </b-popover>
        </template>
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
import { BPopover } from 'bootstrap-vue'

import BoxWrapper from '@/components/BoxWrapper'
import CommentEditor from '@/components/editor/backlog/CommentEditor'
import EmptyColumnPlaceholder from '@/components/posts/EmptyColumnPlaceholder'
import ErrorHandler from '@/mixins/ErrorHandler'
import PostsSelection from '@/components/editor/backlog/PostsSelection'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'NewspaperBacklogBox',

  components: {
    EmptyColumnPlaceholder,
    BoxWrapper,
    CommentEditor,
    PostWrapper,
    PostsSelection,
    BPopover,
  },

  mixins: [ErrorHandler],

  props: {
    newspaper: { type: Object, required: true },
    post: { type: Object, required: true },
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: { type: String, required: true },
    index: { type: Number, required: true }
  },

  data () {
    return {
      editedColumn: null,
      typeOverride: {},
      isPostSelectionOpened: false
    }
  },

  computed: {
    columnIcons () {
      if (this.post.type !== 'box') {
        return []
      }
      if (this.post.css === 'cols-1-1-1') {
        return ['menu-left-col', 'menu-middle-col', 'menu-right-col']
      }
      return ['menu-left-col', 'menu-right-col']
    },

    selected: {
      get () {
        return this.$store.state.backlog.selection[this.post.id]
      },

      set (value) {
        if (value) {
          this.$store.commit('backlog/select', this.post.id)
        } else {
          this.$store.commit('backlog/unselect', this.post.id)
        }
      }
    },

    selectedPost () {
      if (this.post.columns[this.editedColumn].length > 0) {
        return this.post.columns[this.editedColumn].posts.map(p => p.id)
      } else {
        return []
      }
    },

    isAdmin () {
      const { user } = this.$store.state.auth
      return user.isAdmin
    }
  },

  mounted () {
    this._onSelectionOpen = postId => {
      if (this.post.id !== postId) {
        this.closePostSelection()
      }
    }
    this.$root.$on('post-selection-open', this._onSelectionOpen)
  },

  beforeDestroy () {
    this.$root.$off('post-selection-open', this._onSelectionOpen)
  },

  methods: {
    selectBox () {
      this.selected = !this.selected
    },

    renameHeading () {
      const title = window.prompt('Title')
      if (title === null) {
        return
      }

      this.$store.commit('backlog/setBacklogItem', {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        item: {
          id: this.post.id,
          title,
          type: 'header'
        }
      })
    },

    addToColumn ({ post, source, columnIndex = null }) {
      const columns = [...this.post.columns]
      if (columnIndex === null) {
        columnIndex = this.editedColumn
      }
      columns[columnIndex].posts.push({ id: post.id, type: 'post' })
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

    removeFromColumn ({ post, source, index = 0 }) {
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
        items: [{ id: post.id, type: 'post' }],
        index,
        deleteCount: 0
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    editComment (postId) {
      Vue.set(this.typeOverride, postId, CommentEditor)
    },

    closeEditor (postId) {
      Vue.delete(this.typeOverride, postId)
    },

    moveUpInColumn (columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({ id: p.id, type: 'post' }))
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

    moveDownInColumn (columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({ id: p.id, type: 'post' }))
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

    openPostSelection (idx) {
      this.$root.$emit('post-selection-open', this.post.id)
      this.isPostSelectionOpened = true

      Vue.nextTick(() => {
        // make this in next tick and let old dialog close first
        // this cause that PostSelection component will destroyed and recreated immediatelly
        // causing initialPosts property reinitilzed - fixes #506
        this.editedColumn = idx
      })
    },

    closePostSelection () {
      this.editedColumn = null
      this.isPostSelectionOpened = false
    },

    async writeComment (columnIndex) {
      const data = {
        type: 'comment',
        title: '',
        content: ''
      }
      const { post } = await this.$axios.$post('/drafts', data)
      this.$store.commit('backlog/registerPost', {
        newspaper: this.newspaper,
        post
      })
      this.addToColumn({ post, columnIndex })
      this.editComment(post.id)
    },

    async addExternalLink (columnIndex) {
      const url = window.prompt('URL')
      if (url === null) {
        return
      }

      try {
        await this.$store.dispatch('backlog/addLink', {
          newspaper: this.newspaper,
          target: this.source,
          index: this.index,
          columnIndex,
          url
        })
      } catch (err) {
        this.handleError(err)
      }
    },

    toggleEditorialStyle (columnIdx) {
      this.setBacklogItem({
        ...this.post,
        columns: this.post.columns.map((col, idx) => {
          return {
            ...col,
            css:
              columnIdx === idx
                ? col.css === 'editorial'
                  ? ''
                  : 'editorial'
                : col.css
          }
        })
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    moveUp (target = null) {
      this.$store.commit('backlog/moveUp', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    moveDown (target = null) {
      this.$store.commit('backlog/moveDown', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    removePost () {
      this.$store.commit('backlog/remove', {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    setBacklogItem (item) {
      this.$store.commit('backlog/setBacklogItem', {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        item
      })
    },

    makeBox (layout, columnsStyle) {
      this.setBacklogItem({
        // id: this.post.id, // keep same id to keep same NewspaperBacklogBox, NOT GOOD idea as long as post can be removed
        id: Math.random()
          .toString(36)
          .substring(2),
        type: 'box',
        css: layout,
        columns: columnsStyle.map((css, idx) => {
          return {
            css,
            posts: idx === 0 ? [{ id: this.post.id, type: 'post' }] : []
          }
        })
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    splitColumns () {
      this.closePostSelection()
      const posts = []
      this.post.columns.forEach(col =>
        col.posts.forEach(p => posts.push({ id: p.id, type: 'post' }))
      )
      this.$store.commit('backlog/splice', {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        items: posts,
        deleteCount: 1
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
      this.$store.commit('backlog/cleanSelection')
    },

    reverseColumns () {
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
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- Backlog controls
.newspaper-backlog-controls
  position: absolute
  right: (-$baseline * 1.5)
  top: 0

  width: $baseline * 1.25

  @media (max-width: $mobile)
    display: none

  //- button add editorial
  .block-controls
    +button-icon($fa-var-ellipsis-v)

  //- button add comment
  .edit-comment
    +button-icon($fa-var-pencil-alt)

.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
