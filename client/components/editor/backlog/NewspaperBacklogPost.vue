<template>
  <PostWrapper
    :post="log.post"
    :isSubscribed="true"
    :key="log.post.id"
    :editorial="editorType ? {position: editorPosition} : log.editorial"
    @click.native="toggleMobileControls"
  >
    <template #controls>
      <span v-if="log.post.type !== 'comment'" class="price">{{ log.post.price }} Kč</span>
    </template>

    <template #editorial>
      <template v-if="editorType">
        <EditorialCrossroad
          v-if="editorType === 'crossroad'"
          @select="ev => startEditorial(ev, editorPosition)"
        />

        <EditorialArticleEditor
          v-if="editorType === 'article'"
          :newspaper="newspaper"
          :editorial="log.editorial"
          @save="payload => { saveEditorial(payload); cancelEditorialEdit() }"
        />

        <EditorialTweetsEditor
          v-if="editorType === 'tweets'"
          :newspaper="newspaper"
          :editorial="log.editorial"
          @save="payload => { saveEditorial(payload) }"
          @done="cancelEditorialEdit"
        />
      </template>
      <template v-else>
        <component
          v-if="log.editorial"
          :is="'editorial-' + log.editorial.type"
          :editorial="log.editorial">
          <template #controls>&nbsp;</template>
        </component>
      </template>

      <div
        :class="{'newspaper-backlog-controls': true, 'hide-mobile-controls': mobileControls}"
      >
        <div class="newspaper-backlog-controls--arrows">
          <button
            class="up"
            :id="`backlog-controls-up-${log.post.id}`"
            @click.stop="moveUp(log.post.id)"
            :disabled="!canMoveUp"
          ></button>

          <button
            class="down"
            :id="`backlog-controls-down-${log.post.id}`"
            @click.stop="moveDown(log.post.id)"
            :disabled="!canMoveDown"
          ></button>

          <button
            class="remove"
            @click.stop="removePost(log.post.id)"
            v-b-tooltip
            title="Remove post"
          ></button>

          <b-popover
            v-if="source !== 'upcoming'"
            :target="`backlog-controls-up-${log.post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source !== 'upcoming'"
                tabindex="0"
                @click="moveUp(log.post.id, 'upcoming')"
              >
                <h6>{{ $t('Move to upcoming issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source === 'considered'"
                @click="moveUp(log.post.id, 'next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>

          <b-popover
            v-if="source !== 'considered'"
            :target="`backlog-controls-down-${log.post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source === 'upcoming'"
                tabindex="0"
                @click="moveDown(log.post.id, 'next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source !== 'considered'"
                @click="moveDown(log.post.id, 'considered')"
              >
                <h6>{{ $t('Move to backlog issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>
        </div>

        <div
          v-if="log.post.type != 'tweet'"
          class="newspaper-backlog-controls--options">
          <button
            v-if="!log.editorial && !editorType"
            class="add-editorial"
            @click="showCrossroad('right')"
          ></button>

          <template v-else>
            <button
              class="change-position"
              @click="changeEditorialPosition"
              v-b-tooltip
              :title="$t('Change position')"
            ></button>

            <button
              class="menu"
              :id="`backlog-controls-option-${log.post.id}`"
              @click.stop
              v-b-tooltip
              :title="$t('Editorial menu')"
            ></button>

            <b-popover
              :target="`backlog-controls-option-${log.post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li
                  v-show="!editorType"
                  tabindex="0"
                  @click="editEditorial"
                >
                  <h6>{{ $t('Update editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>
                <li
                  v-show="!editorType"
                  tabindex="0"
                  @click="removeEditorial"
                >
                  <h6>{{ $t('Remove editorial') }}</h6>
                  <p>{{ $t('Remove existing editorial') }}</p>
                </li>
                <li
                  v-show="editorType"
                  tabindex="0"
                  @click="cancelEditorialEdit"
                >
                  <h6>{{ $t('Cancel edit') }}</h6>
                  <p>{{ $t('Your changes will be lost') }}</p>
                </li>
              </ul>
            </b-popover>
          </template>

          <button
            v-if="log.post.type == 'comment'"
            class="edit-comment"
            @click="editComment"
          ></button>

        </div>
      </div>
    </template>
  </PostWrapper>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'
import { BPopover } from 'bootstrap-vue'

import PostWrapper from '@/components/PostWrapper'
import NewspaperBacklogInfo from '@/components/editor/backlog/NewspaperBacklogInfo'
import EditorialCrossroad from '@/components/editor/backlog/EditorialCrossroad'
import EditorialArticle from '@/components/posts/EditorialArticle'
import EditorialArticleEditor from '@/components/editor/backlog/EditorialArticleEditor'
import EditorialTweets from '@/components/posts/EditorialTweets'
import EditorialTweetsEditor from '@/components/editor/backlog/EditorialTweetsEditor'

export default {
  name: 'NewspaperBacklogPost',

  components: {
    EditorialCrossroad,
    EditorialArticle,
    EditorialArticleEditor,
    EditorialTweets,
    EditorialTweetsEditor,
    PostWrapper,
    NewspaperBacklogInfo,
    BPopover
  },

  data() {
    return {
      editorType: null,
      editorPosition: null,
      mobileControls: false
    }
  },

  props: {
    newspaper: Object,
    log: Object,
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: String,
  },

  methods: {
    toggleMobileControls() {
      this.mobileControls = !this.mobileControls
    },

    showCrossroad(position) {
      this.startEditorial('crossroad', position)
    },

    startEditorial(type, position) {
      this.editorType = type
      this.editorPosition = position
      this.$root.$emit('bv::hide::popover')
    },

    editEditorial() {
      const { type, position} = this.log.editorial
      this.editorType = type
      this.editorPosition = position
    },

    editComment() {
      this.$router.push(`/posts/${this.log.post.id}`)
    },

    async saveEditorial(payload) {
      await this.$store.dispatch('backlog/saveEditorial', {
        newspaperId: this.newspaper.fullName,
        source: this.source,
        postId: this.log.post.id,
        editorial: {
          ...payload,
          position: this.editorPosition
        }
      })
    },

    cancelEditorialEdit() {
      this.editorType = null
      this.editorPosition = null
      this.$root.$emit('bv::hide::popover')
    },

    removeEditorial() {
      this.$store.dispatch('backlog/removeEditorial', {
        newspaperId: this.newspaper.fullName,
        source: this.source,
        postId: this.log.post.id,
      })
      this.$root.$emit('bv::hide::popover')
    },

    changeEditorialPosition() {
      const { editorPosition, log, newspaper } = this
      if (editorPosition) {
        this.editorPosition = editorPosition === 'left' ? 'right': 'left'
      } else {
        // change existing editorial
        this.$store.dispatch('backlog/saveEditorialPosition', {
          newspaperId: newspaper.fullName,
          source: this.source,
          postId: log.post.id,
          position: log.editorial.position === 'left' ? 'right': 'left'
        })
      }
      this.$root.$emit('bv::hide::popover')
    },

    moveUp(postId, target=null) {
      this.backlogMoveUp({
        newspaper: this.newspaper,
        source: this.source,
        postId,
        target
      })
    },

    moveDown(postId, target=null) {
      this.backlogMoveDown({
        newspaper: this.newspaper,
        source: this.source,
        postId,
        target
      })
    },

    removePost(postId) {
      this.removeFromBacklog({
        newspaper: this.newspaper,
        source: this.source,
        postId
      })
    },

    ...mapActions({
      removeFromBacklog: 'backlog/remove',
      addLinkToBacklog: 'backlog/addLink',
      backlogMoveDown: 'backlog/moveDown',
      backlogMoveUp: 'backlog/moveUp'
    }),
    ...mapMutations({
      showError: 'messages/error'
    })
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


.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
