<template>
  <compotent
    :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    @click.native="toggleMobileControls"
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

      <template v-if="column && column.css === 'editorial'">
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
          class="remove"
          v-b-tooltip
          tabindex="0"
          role="button"
          :title="$t('Remove tweet')"
          @click="removeFromColumn({ post })"
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
          <button
            v-if="post.type !== 'box'"
            class="add-editorial"
            @click="addEditorial"
          />

          <template v-else>
            <button
              class="change-position"
              @click="changeEditorialPosition"
              v-b-tooltip
              :title="$t('Change position')"
            />

            <button
              class="menu"
              :id="`backlog-controls-option-${post.id}`"
              @click.stop
              v-b-tooltip
              :title="$t('Editorial menu')"
            />

            <b-popover
              :target="`backlog-controls-option-${post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li
                  tabindex="0"
                  @click="openPostSelection(null)"
                >
                  <h6>{{ $t('Update editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>

                <li
                  tabindex="1"
                  @click="removeEditorial"
                >
                  <h6>{{ $t('Remove editorial') }}</h6>
                  <p>{{ $t('Remove existing editorial') }}</p>
                </li>
              </ul>
            </b-popover>

            <button
              class="write-comment"
              @click="writeComment"
              v-b-tooltip
              :title="$t('Write comment')"
            />
          </template>
        </div>
      </div>

      <portal to="modal">
        <TweetsSelection
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
import { mapActions  } from 'vuex'
import PostWrapper from '@/components/PostWrapper'
import BoxWrapper from '@/components/BoxWrapper'
import { BPopover } from 'bootstrap-vue'

import TweetsSelection from '@/components/editor/backlog/TweetsSelection'

export default {
  name: 'NewspaperBacklogBox',

  components: {
    PostWrapper,
    BoxWrapper,
    BPopover,
    TweetsSelection,
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
      editedColumn: null
    }
  },

  computed: {
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

    removeFromColumn({ post }) {
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
      this.$store.commit('backlog/prepend', {
        newspaper: this.newspaper,
        target: 'considered',
        item: {id: post.id, type: 'post'}
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    editComment(postId) {

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

    async writeComment() {
      const idx = this.post.columns.findIndex(c => c.css === 'editorial')
      const data = {
        type: 'comment',
        title: '...',
        content: '<p>...</p>'
      }
      const { post } = await this.$axios.$post(`/drafts`, data)
      this.$store.commit('backlog/registerPost', { newspaper: this.newspaper, post })
      this.addToColumn({ post, columnIndex: idx })
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

    addEditorial() {
      this.setBacklogItem({
        id: this.post.id, // keep same id to keep same NewspaperBacklogBox
        type: 'box',
        css: 'cols-2-1',
        columns: [
          { css: '', posts: [{id: this.post.id, type: 'post'}] },
          { css: 'editorial', posts: []}
        ]
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
      this.openPostSelection(1)
    },

    removeEditorial() {
      this.closePostSelection()
      const mainCol = this.post.columns.find(c => c.css !== 'editorial')
      const editorialCol = this.post.columns.find(c => c.css === 'editorial')
      this.setBacklogItem({id: mainCol.posts[0].id, type: 'post'})
      editorialCol.posts.forEach(post => {
        this.$store.commit('backlog/prepend', {
          newspaper: this.newspaper,
          target: 'considered',
          item: {id: post.id, type: 'post'}
        })
      })
      this.$store.dispatch('backlog/save', { newspaper: this.newspaper })
    },

    changeEditorialPosition() {
      this.setBacklogItem({
        ...this.post,
        css: this.post.css === 'cols-2-1' ? 'cols-1-2' : 'cols-2-1',
        columns: [this.post.columns[1], this.post.columns[0]]
      })
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

  @media (max-width: $mobile)
    right: $baseline/4
    top: 40%

  //- button add editorial
  .add-editorial
    +button-icon($fa-var-font)

  //- button add comment
  .edit-comment
    +button-icon($fa-var-pencil-alt)

  //- button menu
  .menu
    +button-icon($fa-var-ellipsis-v)

  //- change position button
  .change-position
    +button-icon($fa-var-exchange-alt)

  .write-comment
    +button-icon($fa-var-feather-alt)


.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
