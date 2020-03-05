<template>
  <compotent
    :is="post.type === 'box' ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    :typeOverride="typeOverride"
    @click.native="toggleMobileControls"
    @close-editor="closeEditor"
  >
    <template #empty-box="{ columnIndex }">
      <EmptyColumnPlaceholder>
        <button
          class="add-posts"
          @click="openPostSelection(columnIndex)"
        >{{ $t('Add posts') }}</button>
        <button
          class="toggle-editorial"
          @click="toggleEditorialStyle(columnIndex)"
        >{{ $t('Toggle editorial') }}</button>
        <button
          class="add-comment"
          @click="writeComment(columnIndex)"
        >{{ $t('Add comment') }}</button>
        <button
          class="add-external"
          @click="addExternalLink(columnIndex)"
        >{{ $t('External article') }}</button>
      </EmptyColumnPlaceholder>
    </template>

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
      <div :class="{'newspaper-backlog-controls': true, 'hide-mobile-controls': mobileControls}">
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

          <button class="remove" @click.stop="removePost()" v-b-tooltip title="Remove post"></button>

          <b-popover
            v-if="source !== 'upcoming'"
            :target="`backlog-controls-up-${post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li v-if="source !== 'upcoming'" tabindex="0" @click="moveUp('upcoming')">
                <h6>{{ $t('Move to upcoming issue') }}</h6>
                <p></p>
              </li>
              <li v-if="source === 'considered'" @click="moveUp('next')">
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
              <li v-if="source === 'upcoming'" tabindex="0" @click="moveDown('next')">
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
              <li v-if="source !== 'considered'" @click="moveDown('considered')">
                <h6>{{ $t('Move to backlog issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>
        </div>

        <div class="newspaper-backlog-controls--options">
          <template v-if="post.type !== 'box' && post.type !== 'header'">
            <button
              class="change-layout"
              :id="`change-layout-${post.id}`"
              v-b-tooltip
              :title="$t('Change layout')"
              @click.stop
            />

            <b-popover
              :target="`change-layout-${post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li tabindex="0" @click="makeBox('cols-2-1', ['', 'editorial'])">
                  <h6>{{ $t('Layout 2-1') }}</h6>
                  <p>{{ $t('One main article, one smaller column') }}</p>
                </li>

                <li tabindex="1" @click="makeBox('cols-1-1', ['', ''])">
                  <h6>{{ $t('Layout 1-1') }}</h6>
                  <p>{{ $t('Two equal sections') }}</p>
                </li>

                <li tabindex="2" @click="makeBox('cols-1-1-1', ['', '', ''])">
                  <h6>{{ $t('Layout 1-1-1') }}</h6>
                  <p>{{ $t('Three equal sections') }}</p>
                </li>
              </ul>
            </b-popover>
          </template>
          <template v-else-if="post.type === 'box'">
            <div class="newspaper-backlog-controls--options--columns">
              <template v-for="(icon, colIndex) in columnIcons">
                <button
                  :class="icon"
                  :id="`backlog-controls-column-options-${post.id}-${colIndex}`"
                  v-b-tooltip
                  :title="$t('Column') + ' ' + (colIndex + 1)"
                  @click.stop
                  :key="`btn-${colIndex}`"
                />

                <b-popover
                  :target="`backlog-controls-column-options-${post.id}-${colIndex}`"
                  placement="bottomleft"
                  triggers="click blur"
                  :key="`btn-popover-${colIndex}`"
                  @click.stop
                >
                  <ul>
                    <li tabindex="0" @click="openPostSelection(colIndex)">
                      <h6>{{ $t('Select posts') }}</h6>
                      <p>{{ $t('Move posts to the column') }}</p>
                    </li>

                    <li tabindex="1" @click="writeComment(colIndex)">
                      <h6>{{ $t('Add comment') }}</h6>
                      <p>{{ $t('Write short comment to the topic') }}</p>
                    </li>

                    <li tabindex="1" @click="addExternalLink(colIndex)">
                      <h6>{{ $t('Add external article') }}</h6>
                      <p>{{ $t('Add article directly') }}</p>
                    </li>

                    <li tabindex="2" @click="toggleEditorialStyle(colIndex)">
                      <h6>{{ $t('Toggle editorial style') }}</h6>
                      <p>{{ $t('Change column background') }}</p>
                    </li>
                  </ul>
                </b-popover>
              </template>
            </div>

            <button
              class="menu"
              v-b-tooltip
              :title="$t('Options')"
              :id="`backlog-controls-layout-options-${post.id}`"
              @click.stop
            />

            <b-popover
              :target="`backlog-controls-layout-options-${post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li tabindex="0" @click="reverseColumns">
                  <h6>{{ $t('Swap columns') }}</h6>
                  <p>{{ $t('Change positions of columns') }}</p>
                </li>

                <li tabindex="1" @click="splitColumns">
                  <h6>{{ $t('Cancel columns') }}</h6>
                  <p>{{ $t('Posts will be bellow each other') }}</p>
                </li>
              </ul>
            </b-popover>
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
import Vue from "vue";
import { mapActions } from "vuex";
import { BPopover } from "bootstrap-vue";


import BoxWrapper from "@/components/BoxWrapper";
import CommentEditor from "@/components/editor/backlog/CommentEditor";
import EmptyColumnPlaceholder from "@/components/posts/EmptyColumnPlaceholder";
import ErrorHandler from '@/mixins/ErrorHandler'
import PostsSelection from "@/components/editor/backlog/PostsSelection";
import PostWrapper from "@/components/PostWrapper";

export default {
  name: "NewspaperBacklogBox",

  mixins: [ErrorHandler],

  components: {
    EmptyColumnPlaceholder,
    BoxWrapper,
    CommentEditor,
    PostWrapper,
    PostsSelection,
    BPopover,
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
    };
  },

  computed: {
    columnIcons() {
      if (this.post.type !== "box") {
        return [];
      }
      if (this.post.css === "cols-1-1-1") {
        return ["menu-left-col", "menu-middle-col", "menu-right-col"];
      }
      return ["menu-left-col", "menu-right-col"];
    },

    isAdmin() {
      const { user } = this.$store.state.auth;
      return user.isAdmin;
    }
  },

  methods: {
    toggleMobileControls() {
      this.mobileControls = !this.mobileControls;
    },

    addToColumn({ post, source, columnIndex = null }) {
      const columns = [...this.post.columns];
      if (columnIndex === null) {
        columnIndex = this.editedColumn;
      }
      columns[columnIndex].posts.push({ id: post.id, type: "post" });
      this.setBacklogItem({
        ...this.post,
        columns
      });
      if (source) {
        this.$store.commit("backlog/remove", {
          newspaper: this.newspaper,
          source,
          postId: post.id
        });
      }
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    removeFromColumn({ post, source, index = 0 }) {
      const columns = [];
      this.post.columns.forEach(col => {
        columns.push({
          ...col,
          posts: col.posts.filter(p => p.id !== post.id)
        });
      });
      this.setBacklogItem({
        ...this.post,
        columns
      });
      this.$store.commit("backlog/splice", {
        newspaper: this.newspaper,
        target: source,
        items: [{ id: post.id, type: "post" }],
        index,
        deleteCount: 0
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    editComment(postId) {
      Vue.set(this.typeOverride, postId, CommentEditor);
    },

    closeEditor(postId) {
      Vue.delete(this.typeOverride, postId);
    },

    moveUpInColumn(columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({ id: p.id, type: "post" }))
        };
        if (idx === columnIndex) {
          const post = col.posts[postIndex];
          col.posts[postIndex] = col.posts[postIndex - 1];
          col.posts[postIndex - 1] = post;
        }
        return col;
      });
      this.setBacklogItem({
        ...this.post,
        columns
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveDownInColumn(columnIndex, postIndex) {
      const columns = this.post.columns.map((col, idx) => {
        col = {
          ...col,
          posts: col.posts.map(p => ({ id: p.id, type: "post" }))
        };
        if (idx === columnIndex) {
          const post = col.posts[postIndex];
          col.posts[postIndex] = col.posts[postIndex + 1];
          col.posts[postIndex + 1] = post;
        }
        return col;
      });
      this.setBacklogItem({
        ...this.post,
        columns
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    openPostSelection(idx) {
      this.$root.$emit("post-selection-open", this.post.id);
      Vue.nextTick(() => {
        // make this in next tick and let old dialog close first
        // this cause that PostSelection component will destroyed and recreated immediatelly
        // causing initialPosts property reinitilzed - fixes #506
        this.editedColumn = idx;
      })
    },

    closePostSelection() {
      this.editedColumn = null;
    },

    async writeComment(columnIndex) {
      const data = {
        type: "comment",
        title: "",
        content: ""
      };
      const { post } = await this.$axios.$post(`/drafts`, data);
      this.$store.commit("backlog/registerPost", {
        newspaper: this.newspaper,
        post
      });
      this.addToColumn({ post, columnIndex });
      this.editComment(post.id);
    },

    async addExternalLink(columnIndex) {
      let url = window.prompt("URL")
      if (url === null) {
        return
      }

      try {
        await this.$store.dispatch('backlog/addLink', {
          newspaper: this.newspaper,
          target: this.source,
          index: this.index,
          columnIndex: columnIndex,
          url
        })
      } catch (err) {
        this.handleError(err)
      }
    },

    toggleEditorialStyle(columnIdx) {
      this.setBacklogItem({
        ...this.post,
        columns: this.post.columns.map((col, idx) => {
          return {
            ...col,
            css:
              columnIdx === idx
                ? col.css === "editorial"
                  ? ""
                  : "editorial"
                : col.css
          };
        })
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveUp(target = null) {
      this.$store.commit("backlog/moveUp", {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    moveDown(target = null) {
      this.$store.commit("backlog/moveDown", {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index,
        target
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    removePost() {
      this.$store.commit("backlog/remove", {
        newspaper: this.newspaper,
        source: this.source,
        index: this.index
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    setBacklogItem(item) {
      this.$store.commit("backlog/setBacklogItem", {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        item
      });
    },

    makeBox(layout, columnsStyle) {
      this.setBacklogItem({
        //id: this.post.id, // keep same id to keep same NewspaperBacklogBox, NOT GOOD idea as long as post can be removed
        id: Math.random()
          .toString(36)
          .substring(2),
        type: "box",
        css: layout,
        columns: columnsStyle.map((css, idx) => {
          return {
            css,
            posts: idx === 0 ? [{ id: this.post.id, type: "post" }] : []
          };
        })
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    splitColumns() {
      this.closePostSelection();
      const posts = [];
      this.post.columns.forEach(col =>
        col.posts.forEach(p => posts.push({ id: p.id, type: "post" }))
      );
      this.$store.commit("backlog/splice", {
        newspaper: this.newspaper,
        target: this.source,
        index: this.index,
        items: posts,
        deleteCount: 1
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    reverseColumns() {
      const columns = [...this.post.columns];
      columns.reverse();
      let css = null;
      if (this.post.css === "cols-2-1") {
        css = "cols-1-2";
      } else if (this.post.css === "cols-1-2") {
        css = "cols-2-1";
      } else {
        css = this.post.css;
      }
      this.setBacklogItem({ ...this.post, css, columns });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    }
  },

  mounted() {
    this._onSelectionOpen = postId => {
      if (this.post.id !== postId) {
        this.closePostSelection();
      }
    };
    this.$root.$on("post-selection-open", this._onSelectionOpen);
  },

  beforeDestroy() {
    this.$root.$off("post-selection-open", this._onSelectionOpen);
  }
};
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'


//- Backlog controls
.newspaper-backlog-controls
  grid-row: 1 / span 1
  grid-column: 1 / span 3

  @media (max-width: $mobile)
    z-index: 5

.newspaper-backlog-controls.hide-mobile-controls
  @media (max-width: $mobile)
    display: none

.newspaper-backlog-controls--arrows
  position: absolute
  left: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-rows: auto auto
  grid-row-gap: $baseline / 4

  @media (max-width: $mobile)
    position: sticky
    left: $baseline/4
    top: $baseline * 2

    height: $baseline * 5
    width: $baseline * 2

  //- button up
  .up
    +button-icon($fa-var-arrow-up)

  //- button down
  .down
    +button-icon($fa-var-arrow-down)

  //- button down
  .remove
    +button-icon($fa-var-times)

.box-header + div > .newspaper-backlog-controls--arrows
  grid-template-rows: 1fr
  grid-column-gap: $baseline / 4
  grid-template-columns: auto auto auto

  @media (max-width: $mobile)
    grid-template-rows: 1fr 1fr
    grid-column-gap: $baseline / 4
    grid-template-columns: $baseline*1.25 1fr $baseline*1.25
    width: calc(100vw - (#{$baseline} * 0.75))

.newspaper-backlog-controls--options
  position: absolute
  right: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-rows: auto auto
  grid-row-gap: $baseline / 4
  width: $baseline * 1.25

  @media (max-width: $mobile)
    position: sticky
    left: calc(100vw - (#{$baseline} * 2))
    top: $baseline * 2


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

  //- options menu
  .menu
    +button-icon($fa-var-ellipsis-v)

//- icons for columns
.newspaper-backlog-controls--options--columns
  white-space: nowrap

  @media (max-width: $mobile)
    display: grid
    grid-template-rows: auto
    grid-row-gap: $baseline / 4

  > button
    margin-right: $baseline / 8

    &:last-of-type
      margin-right: 0

.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
