<template>

  <PostWrapper
    :post="log.post"
    :isSubscribed="true"
    :key="log.post.id"
    :editorial="edit || log.editorial || null"
    @click.native="toggleMobileControls"
  >
    <template slot="extendedControls">
      <span class="price">{{ log.post.price }} Kč</span>
    </template>

    <template slot="controls">
      &nbsp;
    </template>

    <template
      v-if="edit"
      slot="editorial"
    >
      <EditorialArticleEditor
        v-if="edit.type === 'article'"
        :editorial="log.editorial"
        :editor="newspaper.editor"
        @save="ev => saveArticleEditorial(log, ev)"
      />

      <EditorialTweetsEditor
        v-if="edit.type === 'tweets'"
        :tweets="edit.tweets"
        @moveTweetDown="tweet => moveTweetDown(log, tweet)"
        @moveTweetUp="tweet => moveTweetUp(log, tweet)"
        @removeTweet="tweet => removeTweetFromEditorial(log, tweet)"
      />
    </template>

    <template slot="editorialControls" v-if="!log.editorial && !edit">
      <div
        class="editorial-control is-before"
        v-b-tooltip
        title="Add editorial"
        @click="startEditorial('crossroad', log.post.id, 'right')">
      </div>

      <div
        class="editorial-control is-after"
        v-b-tooltip
        title="Add editorial"
        @click="startEditorial('crossroad', log.post.id, 'left')">
      </div>
    </template>

    <template slot="newspaperBacklogControls">
      <div
        class="newspaper-backlog-controls"
        :class="{'hide-mobile-controls': mobileControls[log.post.id]}">
        <div class="newspaper-backlog-controls--arrows">
          <button
            v-show="canMoveUp"
            class="up"
            :id="`backlog-controls-up-${log.post.id}`"
            @click="moveUp(source, log.post.id)">
          </button>
          <button
            v-show="canMoveDown"
            class="down"
            :id="`backlog-controls-down-${log.post.id}`"
            @click="moveDown(source, log.post.id)">
          </button>

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
                @click="moveUp(source, log.post.id, 'upcoming')"
              >
                <h6>Move to upcoming issue</h6>
                <p></p>
              </li>
              <li
                v-if="source === 'considered'"
                @click="moveUp(source, log.post.id, 'next')"
              >
                <h6>Move to next issue</h6>
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
                @click="moveDown(source, log.post.id, 'next')"
              >
                <h6>Move to next issue</h6>
                <p></p>
              </li>
              <li
                v-if="source !== 'considered'"
                @click="moveDown(source, log.post.id, 'considered')"
              >
                <h6>Move to backlog issue</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>
        </div>

        <div class="newspaper-backlog-controls--options">
          <button
            class="menu"
            :id="`backlog-controls-option-${log.post.id}`"
            v-b-tooltip="'Options'"
            @click.stop
          ></button>

          <b-popover
            :target="`backlog-controls-option-${log.post.id}`"
            placement="bottomleft"
            triggers="click blur"
            @click.stop
          >
            <ul>
              <template v-if="(edit || log.editoria) && (edit || log.editoria).position == 'right'">
                <li tabindex="0" @click="changeEditorialPosition(log)">
                  <h6>{{ $t('Display editorial before') }}</h6>
                  <p>{{ $t('On desktop in the left') }}</p>
                </li>
              </template>

              <template v-if="(edit || log.editoria) && (edit || log.editoria).position == 'left'">
                <li tabindex="0" @click="changeEditorialPosition(log)">
                  <h6>{{ $t('Display editorial after') }}</h6>
                  <p>{{ $t('On desktop in the right') }}</p>
                </li>
              </template>

              <template v-if="log.editorial && !edit">
                <li tabindex="0" @click="editEditorial(log)">
                  <h6>{{ $t('Update editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>
                <li tabindex="0" @click="removeEditorial(log)">
                  <h6>{{ $t('Remove editorial') }}</h6>
                  <p>{{ $t('Remove existing editorial') }}</p>
                </li>
              </template>
              <template v-if="edit">
                <li tabindex="0" @click="cancelEditorialEdit(log)">
                  <h6>{{ $t('Cancel edit') }}</h6>
                  <p>{{ $t('Your changes will be lost') }}</p>
                </li>
              </template>
              <template v-if="!log.editorial && !edit">
                <!-- <li tabindex="0" @click="startEditorial('article', log.post.id)">
                  <h6>{{ $t('Add editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>
                <li tabindex="0" @click="startEditorial('tweets', log.post.id)">
                  <h6>{{ $t('Add editorial tweet(s)') }}</h6>
                  <p>{{ $t('Comment the topic using tweets') }}</p>
                </li> -->
                <li tabindex="0" @click="startEditorial('crossroad', log.post.id, 'right')">
                  <h6>Add editorial</h6>
                  <p>Either your comment or tweets</p>
                </li>
              </template>

              <li tabindex="0" @click="removePost(source, log.post.id)">
                <h6>Remove post</h6>
                <p>Post won't be consider anymore</p>
              </li>
            </ul>
          </b-popover>
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
import EditorialArticleEditor from '@/components/posts/EditorialArticleEditor'
import EditorialTweetsEditor from '@/components/posts/EditorialTweetsEditor'

export default {
  name: 'NewspaperBacklogPost',

  components: {
    EditorialArticleEditor,
    EditorialTweetsEditor,
    PostWrapper,
    NewspaperBacklogInfo,
    BPopover
  },

  data() {
    return {
      edit: null,
      //tweetsTarget: null, // TODO move this up
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

    startEditorial(type, postId, position) {
      const edit = {
        type,
        position: position
      }
      if (type === 'tweets') {
        this.tweetsTarget = postId
        edit.tweets = []
      }

      this.edit = edit
      this.$root.$emit('bv::hide::popover')
    },

    editEditorial(log) {
      const postId = log.post.id
      const { type, position, tweets} = log.editorial
      const edit = {
        type: type,
        position: position,
      }
      if (type === 'tweets') {
        this.tweetsTarget = postId
        edit.tweets = [...tweets]
      }
      this.edit = edit
    },

    saveArticleEditorial(log, { title, content}) {
      const postId = log.post.id
      this.$store.dispatch('saveEditorial', {
        newspaperId: this.newspaper.fullName,
        postId: postId,
        editorial: {
          type: 'article',
          title: title,
          content: content,
          position: this.edit.position
        }
      })
      this.edit = null
    },

    async saveTweetsEditorial(log, tweets) {
      const postId = log.post.id
      const editorial = await this.$store.dispatch('saveEditorial', {
        newspaperId: this.newspaper.fullName,
        postId: postId,
        editorial: {
          type: 'tweets',
          tweets: tweets.map(t => t.id),
          position: this.edit.position
        }
      })
      // update content with server side version
      edit.tweets = [...editorial.tweets]
    },

    cancelEditorialEdit(log) {
      this.edit = null
      if (this.tweetsTarget === log.post.id) {
        this.tweetsTarget = null
      }
      this.$root.$emit('bv::hide::popover')
    },

    removeEditorial(log) {
      this.$store.dispatch('removeEditorial', {
        newspaperId: this.newspaper.fullName,
        postId: log.post.id,
      })
      this.$root.$emit('bv::hide::popover')
    },

    changeEditorialPosition(log) {
      if (this.edit) {
        this.edit.position = this.edit.position === 'left' ? 'right': 'left'
      } else {
        // change existing editorial
        this.$store.dispatch('saveEditorialPosition', {
          newspaperId: this.newspaper.fullName,
          postId: log.post.id,
          position: log.editorial.position === 'left' ? 'right': 'left'
        })
      }
      this.$root.$emit('bv::hide::popover')
    },

    addTweetToEditorial({ post }) {
      const log = this.published.find(l => l.post.id === this.tweetsTarget)
      const { tweets } = this.editorialEditors[this.tweetsTarget]
      tweets.push(post)
      // TODO this is hack
      this.$store.dispatch('removeFromBacklogLocal', {
        newspaper: this.newspaper,
        post: post,
      })
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    removeTweetFromEditorial(log, tweet) {
      const { tweets } = this.editorialEditors[this.tweetsTarget]
      const idx = tweets.indexOf(tweet)
      tweets.splice(idx, 1)
      // TODO this is hack
      this.$store.dispatch('addToBacklogLocal', {
        newspaper: this.newspaper,
        post: tweet,
      })
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    moveTweetDown(log, tweet) {
      const { tweets } = this.editorialEditors[this.tweetsTarget]
      const idx = tweets.indexOf(tweet)
      tweets[idx] = tweets[idx + 1]
      tweets[idx + 1] = tweet
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    moveTweetUp(log, tweet) {
      const { tweets } = this.editorialEditors[this.tweetsTarget]
      const idx = tweets.indexOf(tweet)
      tweets[idx] = tweets[idx - 1]
      tweets[idx - 1] = tweet
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    moveUp(source, postId, target=null) {
      this.backlogMoveUp({
        newspaper: this.newspaper,
        source,
        postId,
        target
      })
    },

    moveDown(source, postId, target=null) {
      this.backlogMoveDown({
        newspaper: this.newspaper,
        source,
        postId,
        target
      })
    },

    removePost(source, postId) {
      this.removeFromNewspaperBacklog({
        newspaper: this.newspaper,
        source,
        postId
      })
    },

    ...mapActions([
      'removeFromNewspaperBacklog', 'addLinkToBacklog',
      'backlogMoveDown', 'backlogMoveUp'
      //, 'backlogMoveTo'

    ]),
    ...mapMutations(['showError'])
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- Editorial Controls
.editorial-control
  position: absolute
  top: 0

  height: 100%
  width: $baseline / 2

  cursor: pointer

  &:hover
    background: #eee

  &.is-before
    right: 0

  &.is-after
    left: 0

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

  //- button up
  .menu
    +button-icon($fa-var-ellipsis-v)


</style>
