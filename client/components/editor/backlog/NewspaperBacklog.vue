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

  props: {
    newspaper: Object,
    backlog: Array,
    published: Array,
    currentMonth: Object,
  },

  methods: {
    async publishBacklog() {
      const { fullName } = this.newspaper
      const postIds = this.published.map(p => p.id)
      await this.$axios.post(`/newspapers/${fullName}/backlog/publish`, postIds)
    },


    publish(post) {
      this.backlog.splice(this.backlog.indexOf(post), 1)
      this.published.push(post)
      this.publishBacklog()
      this.backlogSetPostState({newspaper: this.newspaper, post: post, state: 'P'})
    },

    undoPublish(post) {
      this.published.splice(this.published.indexOf(post), 1)
      this.backlog.push(post)
      this.publishBacklog()
      this.backlogSetPostState({newspaper: this.newspaper, post: post, state: 'C'})
    },

    moveUp(idx) {
      const post = this.published[idx]
      Vue.set(this.published, idx, this.published[idx - 1])
      Vue.set(this.published, idx - 1, post)
      this.publishBacklog()
    },

    moveDown(idx) {
      const post = this.published[idx]
      Vue.set(this.published, idx, this.published[idx + 1])
      Vue.set(this.published, idx + 1, post)
      this.publishBacklog()
    },

    removePost(post) {
      this.backlog.splice(this.backlog.indexOf(post), 1)
      this.removeFromBacklog({newspaper: this.newspaper, post: post})
    },

    ...mapActions(['removeFromBacklog']),
    ...mapMutations(['backlogSetPostState'])
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



</style>
