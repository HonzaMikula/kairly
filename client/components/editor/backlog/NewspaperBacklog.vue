<template>
  <div class="newspaper-backlog-view">

    <NewspaperBacklogInfo
      :newspaper="newspaper"
      :current-month="currentMonth"
      :backlog-length="backlog.length"
      :published="published"
    />

    <div>
      <div class="newspaper-backlog--next-issue">
        <div v-if="published.length == 0" class="no-post">
          <h2>{{ $t('No posts for the upcoming issue!') }}</h2>

          <p>{{ $t('Drag articles and tweets from the right panel that you want to publish in next issue of the newspaper.') }}</p>
        </div>

        <PostWrapper
          v-for="(post, idx) in published"
          :post="post"
          :isSubscribed="true"
          :key="post.id"
          :editorial="editorial[post.id]"
          :editorialPosition="editorialPosition[post.id]"
        >
          <template slot="extendedControls">
            <span class="price">{{ post.price }} Kč</span>
          </template>

          <template slot="controls">
            <button-icon
              class="editorial"
              v-b-tooltip="$t('Add editorial')"
              tabindex="0"
              role="button"
              :id="`editorial-button-${post.id}`"
              :class="{'is-active': editorial[post.id]}"
            />

            <b-popover
              :target="`editorial-button-${post.id}`"
              placement="auto"
              triggers="click blur"  
            >
              <ul>
                <template v-if="!editorial[post.id]">
                  <li tabindex="0" @click="setEditorial('article', post.id)">
                    <h6>Add editorial comment</h6>
                    <p>Write short comment to the topic</p>
                  </li>
                  <li tabindex="0" @click="setEditorial('tweet', post.id)">
                    <h6>Add editorial tweet(s)</h6>
                    <p>Comment the topic using tweets</p>
                  </li>
                </template>

                <template v-else> 
                  <li tabindex="0" @click="changeEditorialPosition(post.id)">
                    <h6>Display editorial before</h6>
                    <p>On desktop in the left</p>
                  </li>
                  <li tabindex="0" @click="removeEditorial(post.id)">
                    <h6>Remove editorial</h6>
                    <p>Your changes will be lost</p>
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
              @click.prevent="undoPublish(post)"
            />
          </template>
        </PostWrapper>
      </div>

      <div class="newspaper-backlog--backlog">
        <div class="newspaper-backlog--backlog--external-article">
          <input
            type="url"
            v-model="externalLink"
            placeholder="Paste URL of external article"
          />
          <button
            @click.prevent="addExternalLink">
            Add article
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
          v-for="post in backlog"
          :key="post.id"
          :post="post"
          @publish="publish(post)"
          @remove="removePost(post)"
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

export default {
  name: 'NewspaperBacklog',

  components: {
    PostWrapper,
    NewspaperBacklogInfo,
    BacklogPost,
    BPopover
  },

  data() {
    return {
      externalLink: null,
      editorial: [],
      editorialPosition: []
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
    currentMonth() {
      return this.newspaperBacklog ? this.newspaperBacklog.currentMonthStats : []
    }
  },

  methods: {
    setEditorial (type, postId) {
      this.editorial[postId] = type
      this.$forceUpdate()
    },

    removeEditorial(postId) {
      this.editorial[postId] = null
      this.$forceUpdate()
    },

    changeEditorialPosition(postId) {
      this.editorialPosition[postId] = !this.editorialPosition[postId]
      this.$forceUpdate()
    },

    publish(post) {
      this.backlogPublish({newspaper: this.newspaper, post})
    },

    undoPublish(post) {
      this.backlogUndoPublish({newspaper: this.newspaper, post})
    },

    moveUp(index) {
      this.backlogMoveUp({newspaper: this.newspaper, index})
    },

    moveDown(index) {
      this.backlogMoveDown({newspaper: this.newspaper, index})
    },

    removePost(post) {
      this.removeFromNewspaperBacklog({newspaper: this.newspaper, post})
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
