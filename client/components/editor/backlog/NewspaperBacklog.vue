<template>
  <div class="newspaper-backlog-view">

    <NewspaperBacklogInfo
      :newspaper="newspaper"
      :current-month="currentMonth"
      :backlog-length="backlog.length"
      :published="published.map(log => log.post)"
    />

    <div>
      <div class="newspaper-backlog--next-issue">
        <div v-if="published.length == 0" class="no-post">
          <h2>{{ $t('No posts for the upcoming issue!') }}</h2>

          <p>{{ $t('Drag articles and tweets from the right panel that you want to publish in next issue of the newspaper.') }}</p>
        </div>

        <PostWrapper
          v-for="([log, edit], idx) in publishedWithEditor"
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
              v-show="idx !== 0"
              class="up"
              v-b-tooltip
              tabindex="0"
              role="button"
              :title="$t('Move post up')"
              @click="moveUp(idx)"
            />

            <button-icon
              v-show="idx !== published.length - 1"
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
              :title="$t('Remove from issue')"
              @click.prevent="undoPublish(log)"
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
              @removeTweet="tweet => removeTweetFromEditorial(log, tweet)"
            />
          </template>
        </PostWrapper>
      </div>

      <div class="newspaper-backlog--backlog">
        <div class="newspaper-backlog--backlog--external-article">
          <input
            type="url"
            v-model="externalLink"
            :placeholder="$t('Paste URL of external article')"
          />
          <button
            @click.prevent="addExternalLink">
            {{ $t('Add article') }}
          </button>
        </div>

        <div
          v-if="backlog.length == 0"
          class="no-post"
        >
          <h2>{{ $t('No considered posts!') }}</h2>

          <p>{{ $t('Go on your timeline and start adding interesting articles and tweets for considaration.') }}</p>
        </div>

        <BacklogPost
          v-for="log in backlog"
          :key="log.post.id"
          :post="log.post"
          :isTweersEditorialOpen="!!tweetsTarget"
          @addToEditorial="addTweetToEditorial(log)"
          @publish="publish(log)"
          @remove="removePost(log)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'
import { BPopover } from 'bootstrap-vue'

import PostWrapper from '@/components/PostWrapper'
import NewspaperBacklogInfo from '@/components/editor/backlog/NewspaperBacklogInfo'
import BacklogPost from '@/components/editor/backlog/BacklogPost'
import EditorialArticleEditor from '@/components/posts/EditorialArticleEditor'
import EditorialTweetsEditor from '@/components/posts/EditorialTweetsEditor'
import PostWrapperVue from '../../PostWrapper.vue';

export default {
  name: 'NewspaperBacklog',

  components: {
    BacklogPost,
    BPopover,
    EditorialArticleEditor,
    EditorialTweetsEditor,
    PostWrapper,
    NewspaperBacklogInfo,
  },

  data() {
    return {
      externalLink: null,
      editorialEditors: {},
      tweetsTarget: null
    }
  },

  props: {
    newspaper: Object
  },

  computed: {
    newspaperBacklog() {
      return this.$store.state.newspaperBacklog[this.newspaper.fullName]
    },
    backlog() {
      return this.newspaperBacklog ? this.newspaperBacklog.postsBacklog : []
    },
    published() {
      return this.newspaperBacklog ? this.newspaperBacklog.postsPublished : []
    },
    publishedWithEditor() {
      return this.published.map(log => [log, this.editorialEditors[log.post.id]])
    },
    currentMonth() {
      return this.newspaperBacklog ? this.newspaperBacklog.currentMonthStats : []
    }
  },

  methods: {
    startEditorial(type, postId) {
      const edit = {
        type,
        position: 'right'
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
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    removeTweetFromEditorial(log, tweet) {
      const { tweets } = this.editorialEditors[this.tweetsTarget]
      const idx = tweets.indexOf(tweet)
      tweets.splice(idx, 1)
      this.saveTweetsEditorial(log, tweets)
      this.$root.$emit('bv::hide::popover')
    },

    publish(log) {
      this.backlogPublish({newspaper: this.newspaper, log})
    },

    undoPublish(log) {
      this.backlogUndoPublish({newspaper: this.newspaper, log})
    },

    moveUp(index) {
      this.backlogMoveUp({newspaper: this.newspaper, index})
    },

    moveDown(index) {
      this.backlogMoveDown({newspaper: this.newspaper, index})
    },

    removePost(log) {
      this.removeFromNewspaperBacklog({newspaper: this.newspaper, log})
    },

    async addExternalLink() {
      const url = this.externalLink
      if (!url) {
        return
      }

      this.$ga.event({
        eventCategory: 'Add external article',
        eventAction: url,
        eventLabel: this.newspaper
      })

      try {
        await this.addLinkToBacklog({newspaper: this.newspaper, url})
        this.externalLink = ''
      } catch (err) {
        if (err.response.status >= 400) {
          this.showError(err.response.data.error)
        } else {
          this.showError((err + '') || 'Request failed')
        }
      }
    },

    ...mapActions([
        'removeFromNewspaperBacklog', 'addLinkToBacklog',
        'backlogMoveDown', 'backlogMoveUp',
        'backlogPublish', 'backlogUndoPublish'
    ]),
    ...mapMutations(['showError'])
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

.newspaper-backlog-view
  > div
    display: grid
    grid-template-columns: 970px auto
    grid-column-gap: $baseline


p.newspaper-backlog--info--profit
  strong
    margin-right: $baseline / 2

    color: $c-base

    cursor: pointer

    &:hover,
    &:focus
      darken($c-base, 10%)


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

//- Backlog
.newspaper-backlog--backlog
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

      content: fa-content($fa-var-newspaper)

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center


//- Add external article
.newspaper-backlog--backlog--external-article
  display: flex
  margin-bottom: $baseline

  input[type=url]
    border: 1px solid #ddd
    border-right: 0
    border-radius: 3px 0 0 3px
    box-sizing: border-box
    flex: 1
    height: $baseline * 1.25
    padding: 0 $baseline/4

    font-family: $ff-sans
    font-size: $fs--1

  button
    border-radius: 0 3px 3px 0
    box-sizing: border-box
    height: $baseline * 1.25

    background: $c-base
    border: 0
    color: #fff

    font-family: $ff-sans
    font-size: $fs--1

    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)

</style>
