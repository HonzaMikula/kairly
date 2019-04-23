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
        >
          <template slot="extendedControls">
            <span class="price">{{ post.price }} Kč</span>
          </template>

          <template slot="controls">
            <button-icon
              v-show="idx !== 0"
              class="up"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              tabindex="0"
              role="button"
              :title="$t('Move post up')"
              @click="moveUp(idx)"
            />

            <button-icon
              v-show="idx !== published.length - 1"
              class="down"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
              tabindex="0"
              role="button"
              :title="$t('Move post down')"
              @click="moveDown(idx)"
            />

            <button-icon
              class="remove"
              v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
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

import PostWrapper from '@/components/PostWrapper'
import NewspaperBacklogInfo from '@/components/editor/backlog/NewspaperBacklogInfo'
import BacklogPost from '@/components/editor/backlog/BacklogPost'

export default {
  name: 'NewspaperBacklog',

  components: {
    PostWrapper,
    NewspaperBacklogInfo,
    BacklogPost
  },

  data() {
    return {
      externalLink: null
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
