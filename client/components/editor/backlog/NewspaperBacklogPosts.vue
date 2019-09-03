<template>
  <div class="newspaper-editor-backlog-section">
    <header class="newspaper-editor-backlog--heading">
      <h2>{{ title }}</h2>

      <button @click="() => expanded = !expanded" :class="{'is-expanded': expanded}"></button>

      <p>{{ description }}</p>

    </header>

    <div
      v-show="expanded"
      class="newspaper-backlog--next-issue"
    >


      <div v-if="backlogWithEditor.length == 0" class="no-post">
        <h2>{{ $t('No posts in backlog') }}</h2>
      </div>

      <PostWrapper
        v-for="([log, edit], idx) in backlogWithEditor"
        :post="log.post"
        :isSubscribed="true"
        :key="log.post.id"
        :editorial="edit || log.editorial || null"
      >
        <template slot="extendedControls">
          <span class="price">{{ log.post.price }} Kč</span>
        </template>

        <template slot="controls">
          <button-icon
            v-if="log.post.type != 'tweet'"
            class="editorial"
            v-b-tooltip="$t('Add editorial')"
            tabindex="0"
            role="button"
            :id="`editorial-button-${log.post.id}`"
            :class="{'is-active': edit}"
          />

          <b-popover
            :target="`editorial-button-${log.post.id}`"
            placement="auto"
            triggers="click blur"
          >
            <ul>
              <template v-if="((log.editorial || edit)) && (editorialEditors[log.post.id] && editorialEditors[log.post.id].position == 'right')">
                <li tabindex="0" @click="changeEditorialPosition(log)">
                  <h6>{{ $t('Display editorial before') }}</h6>
                  <p>{{ $t('On desktop in the left') }}</p>
                </li>
              </template>

              <template v-if="((log.editorial || edit)) && (editorialEditors[log.post.id] && editorialEditors[log.post.id].position == 'left')">
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
                <li tabindex="0" @click="startEditorial('article', log.post.id)">
                  <h6>{{ $t('Add editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>
                <li tabindex="0" @click="startEditorial('tweets', log.post.id)">
                  <h6>{{ $t('Add editorial tweet(s)') }}</h6>
                  <p>{{ $t('Comment the topic using tweets') }}</p>
                </li>
              </template>
            </ul>
          </b-popover>

          <button-icon
            v-show="publishIssue !== 1 || idx !== 0"
            class="up"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move post up')"
            @click="moveUp(idx)"
          />

          <button-icon
            v-show="publishIssue !== null || idx < backlogWithEditor.length - 1"
            class="down"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Move post down')"
            @click="moveDown(idx)"
          />

          <button-icon
            class="remove"
            v-b-tooltip
            tabindex="0"
            role="button"
            :title="$t('Remove from backlog')"
            @click.prevent="removePost(log)"
          />
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
        
      </PostWrapper>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'
import { BPopover } from 'bootstrap-vue'

import PostWrapper from '@/components/PostWrapper'
import NewspaperBacklogInfo from '@/components/editor/backlog/NewspaperBacklogInfo'
import EditorialArticleEditor from '@/components/posts/EditorialArticleEditor'
import EditorialTweetsEditor from '@/components/posts/EditorialTweetsEditor'
import PostWrapperVue from '../../PostWrapper.vue';

export default {
  name: 'NewspaperBacklogPosts',

  components: {
    EditorialArticleEditor,
    EditorialTweetsEditor,
    PostWrapper,
    NewspaperBacklogInfo,
    BPopover
  },

  data() {
    return {
      editorialEditors: {},
      tweetsTarget: null,
      expanded: true,
    }
  },

  props: {
    newspaper: Object,
    title: String,
    description: String,
    backlog: Array,
    publishIssue: Number,
    baseIndex: Number,
  },

  computed: {
    backlogWithEditor() {
      return this.backlog.map(log => [log, this.editorialEditors[log.post.id]])
    },
  },

  methods: {
    startEditorial(type, postId, position) {
      const edit = {
        type,
        position: position
      }
      if (type === 'tweets') {
        this.tweetsTarget = postId
        edit.tweets = []
      }

      Vue.set(this.editorialEditors, postId, edit)
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
      Vue.set(this.editorialEditors, postId, edit)

    },

    saveArticleEditorial(log, { title, content}) {
      const postId = log.post.id
      const edit = this.editorialEditors[postId]
      this.$store.dispatch('saveEditorial', {
        newspaperId: this.newspaper.fullName,
        postId: postId,
        editorial: {
          type: 'article',
          title: title,
          content: content,
          position: edit.position
        }
      })
      Vue.delete(this.editorialEditors, postId)
    },

    async saveTweetsEditorial(log, tweets) {
      const postId = log.post.id
      const edit = this.editorialEditors[postId]
      const editorial = await this.$store.dispatch('saveEditorial', {
        newspaperId: this.newspaper.fullName,
        postId: postId,
        editorial: {
          type: 'tweets',
          tweets: tweets.map(t => t.id),
          position: edit.position
        }
      })
      // update content with server side version
      edit.tweets = [...editorial.tweets]
    },

    cancelEditorialEdit(log) {
      const postId = log.post.id
      Vue.delete(this.editorialEditors, postId)
      if (this.tweetsTarget === postId) {
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
      const edit = this.editorialEditors[log.post.id]
      if (edit) {
        edit.position = edit.position === 'left' ? 'right': 'left'
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

    // publish(log) {
    //   this.backlogPublish({newspaper: this.newspaper, log})
    // },

    // undoPublish(log) {
    //   this.backlogUndoPublish({newspaper: this.newspaper, log})
    // },

    moveUp(index) {
      if (index === 0) {
        this.backlogMoveTo({
          newspaper: this.newspaper,
          index: this.baseIndex + index,
          publish: this.publishIssue === null ? 2 : this.publishIssue - 1
        })
      } else {
        this.backlogMoveUp({
          newspaper: this.newspaper,
          index: this.baseIndex + index,
        })
      }
    },

    moveDown(index) {
      if (index === this.backlog.length - 1) {
        this.backlogMoveTo({
          newspaper: this.newspaper,
          index: this.baseIndex + index,
          publish: this.publishIssue === 2 ? null : this.publishIssue + 1
        })
      } else {
        this.backlogMoveDown({
          newspaper: this.newspaper,
          index: this.baseIndex + index
        })
      }
    },

    removePost(log) {
      this.removeFromNewspaperBacklog({newspaper: this.newspaper, log})
    },

    ...mapActions([
      'removeFromNewspaperBacklog', 'addLinkToBacklog',
      'backlogMoveDown', 'backlogMoveUp', 'backlogMoveTo'
    ]),
    ...mapMutations(['showError'])
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

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

  //- expand button
  button
    +button-icon($fa-var-plus, icon, solid)
    grid-column: 1
    grid-row: 1
    background: #fafafa

    &.is-expanded
      +button-icon($fa-var-minus, icon, solid)
      background: #fafafa

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
</style>
