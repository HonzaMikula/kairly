<template>
  <newspaper-backlog-view>

    <newspaper-backlog--info>
      <div>
        Issue <strong>#{{newspaper.issues + 1}}</strong> will be automatically
        published in <strong :title="newspaper.nextRelease">{{ timeFrom(newspaper.nextRelease) }}</strong>
      </div>

      <div>
        <strong>{{backlog.length}} posts</strong> are considered
      </div>
    </newspaper-backlog--info>

    <div>
      <newspaper-backlog--next-issue>
        <div v-if="published.length == 0" class="no-post">
          <h2>No posts for the upcoming issue!</h2>

          <p>Drag articles and tweets from the right panel that you want to publish in next issue of the newspaper.</p>
        </div>

        <PostWrapper
          v-for="(post, idx) in published"
          :post="post"
          :isSubscribed="true"
          :key="post.id"
        >
          <template slot="extendedControls">
            &nbsp;
          </template>

          <template slot="controls">
            <button-icon
              class="up" aria-label="Move post up"
              v-tooltip.top="'Move post up'"
              v-show="idx !== 0"
              @click="moveUp(idx)">
            </button-icon>

            <button-icon
              class="down" aria-label="Move post down"
              v-tooltip.top="'Move post down'"
              v-show="idx !== published.length - 1"
              @click="moveDown(idx)">
            </button-icon>

            <button-icon
              class="remove" aria-label="Remove from issue"
              v-tooltip.top="'Remove from issue'"
              @click.prevent="undoPublish(post)">
            </button-icon>
          </template>
        </PostWrapper>
      </newspaper-backlog--next-issue>

      <newspaper-backlog--backlog>
        <div v-if="backlog.length == 0" class="no-post">
          <h2>No considered posts!</h2>

          <p>Go on your timeline and start adding interesting articles and tweets for considaration.</p>
        </div>

        <div v-for="post in backlog" class="backlog-post" :key="post.id">
          <header>
            <picture>
              <router-link :to="{name: 'author', params: {author: post.author.id}}">
                <img :src="post.author.picture" :alt="post.author.name" />
              </router-link>
            </picture>

            <h3>
              <router-link :to="{name: 'author', params: {author: post.author.id}}">
                {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
              </router-link>
            </h3>

            <time>
              {{ post.time | moment('calendar') }}
              •
              {{ post.timeRead }} read
            </time>

            <section>
              <button-icon
                class="remove"
                role="button"
                aria-label="Remove post from considaration"
                v-tooltip.top.end="'Remove post from considaration'"
                @click.prevent="removePost(post)">
              </button-icon>

              <a href="#" @click.prevent="publish(post)">Publish</a>
            </section>

          </header>

          <template v-if="post.type == 'tweet'">
            <p v-html="post.content.content"></p>
          </template>

          <template v-else>
            <h2><router-link :to="{ name: 'post', params: { postId: post.id }}">{{ post.content.title }}</router-link></h2>
          </template>
        </div>
      </newspaper-backlog--backlog>
    </div>
  </newspaper-backlog-view>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'
import moment from 'moment'

import * as api from '@/api'

import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'NewspaperBacklog',

  components: {
    PostWrapper
  },

  props: {
    newspaper: Object
  },

  data() {
    return {
      backlog: [],
      published: []
    }
  },

  methods: {
    timeFrom(dt) {
      return moment(dt).from()
    },

    init() {
      api.getNewspaperBacklog(this.newspaper.fullName).then(resp => {
        this.backlog = resp.backlog
        this.published = resp.publish
      })
    },

    publish(post) {
      this.backlog.splice(this.backlog.indexOf(post), 1)
      this.published.push(post)
      api.publishBacklog(this.newspaper.fullName, this.published.map(p => p.id))
      .catch(this.init)
      this.backlogSetPostState({newspaper: this.newspaper, post: post, state: 'P'})
    },

    undoPublish(post) {
      this.published.splice(this.published.indexOf(post), 1)
      this.backlog.push(post)
      api.publishBacklog(this.newspaper.fullName, this.published.map(p => p.id))
      .catch(this.init)
      this.backlogSetPostState({newspaper: this.newspaper, post: post, state: 'C'})
    },

    moveUp(idx) {
      const post = this.published[idx]
      Vue.set(this.published, idx, this.published[idx - 1])
      Vue.set(this.published, idx - 1, post)
      api.publishBacklog(this.newspaper.fullName, this.published.map(p => p.id))
      .catch(this.init)
    },

    moveDown(idx) {
      const post = this.published[idx]
      Vue.set(this.published, idx, this.published[idx + 1])
      Vue.set(this.published, idx + 1, post)
      api.publishBacklog(this.newspaper.fullName, this.published.map(p => p.id))
      .catch(this.init)
    },

    removePost(post) {
      this.removeFromBacklog({newspaper: this.newspaper, post: post})
      this.init()
    },

    ...mapActions(['removeFromBacklog']),
    ...mapMutations(['backlogSetPostState'])
  },

  created() {
    this.init()

    this.$watch('newspaper', newspaper => {
      this.init()
    })
  }
}
</script>

<style lang="sass">
newspaper-backlog-view
  > div
    display: grid
    grid-template-columns: 970px auto
    grid-column-gap: $baseline
    min-height: 50vh


//- Info when release go out
newspaper-backlog--info
  display: grid
  grid-template-columns: 970px auto
  grid-column-gap: $baseline

  padding: $baseline/4 0
  margin-bottom: $baseline

  border-bottom: 1px solid #ddd
  border-top: 1px solid #ddd

  font-size: $fs--1
  font-family: $ff-serif
  text-align: center

//- Next Issue
newspaper-backlog--next-issue
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

      display: block
      margin-bottom: $baseline

      font-size: $fs-4

      content: $fa-var-clock-o

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center

//- Backlog
newspaper-backlog--backlog
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

      display: block
      margin-bottom: $baseline

      font-size: $fs-4

      content: $fa-var-newspaper-o

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center


  //- post
  .backlog-post
    padding: $baseline / 4
    margin-bottom: $baseline / 2
    background: #fff

    //- article
    h2
      font-weight: 600
      font-family: $ff-serif

      a
        color: #000

    //- tweet
    p
      font-family: $ff-serif
      font-size: $fs-1


    > header
      position: relative

      display: grid
      grid-template-areas: "picture author" "picture info"
      grid-template-columns: 52px 1fr auto
      grid-template-rows: 0.75*$baseline 0.75*$baseline
      margin-bottom: $baseline / 2

      font-family: $ff-sans

      //-- author image
      picture
        grid-area: picture

        img
          border-radius: 100%
          height: $baseline * 1.5
          margin-right: $baseline / 2
          width: $baseline * 1.5

          object-fit: cover


      //-- author
      h3
        grid-area: author
        max-width: max-content

        color: $c-base

        font-size: $fs--2
        line-height: $baseline * 0.75

        a
          color: $c-base


      //-- date of publication
      time
        grid-area: info
        width: 100%

        color: #999

        font-size: $fs--2
        line-height: $baseline * 0.75

      //-- controls
      section
        > a
          display: inline-block
          border-radius: 3px
          padding: 0 $baseline/2
          margin-left: $baseline / 4

          background: $c-base
          color: #fff

          font-size: $fs--1

          &:focus,
          &:hover
            background: darken($c-base, 10%)

        button-icon
          opacity: 0.2

          &:focus,
          &:hover
            opacity: 1

</style>
