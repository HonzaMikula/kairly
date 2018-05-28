<template>
  <author-detail-view
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loadingPosts"
    infinite-scroll-distance="100"
  >
    <loading-spinner v-if="loadingProfile"></loading-spinner>

    <div v-else>
      <author-detail--header>
        <picture>
          <img :src="author.picture" :alt="author.name"/>
        </picture>
        <h1>{{ author.name }}</h1>
        <p>{{ author.bio }}</p>
      </author-detail--header>

      <author-detail--subscribe>
        <button
          v-if="author.isSubscribed"
          class="is-subscribed"
          v-on:click="unfollow($event)">
          Unsubscribe author
        </button>

        <button 
          v-else
          v-on:click="openSubscribeWidget()">
          Subscribe author
        </button>

        <follow-author 
          v-if="subscribeStep != null"
          v-on-clickaway="() => closeSubscribeWidget()">
          <section v-if="subscribeStep == 1">
            <header>How often?</header>
            <ul>
              <li><a href="" v-on:click.prevent="selectHowOften('3X', $event)">3x per day</a></li>
              <li><a href="" v-on:click.prevent="selectHowOften('daily', $event)">Daily</a></li>
              <li><a href="" v-on:click.prevent="selectHowOften('weekly', $event)">Weekly</a></li>
            </ul>
          </section>

          <section v-if="subscribeStep == 4">
            <header>You're subscribed!</header>
            <div v-if="subscribePeriod == '3X'">
              <p>
                You will be receiving <strong>{{ author.name }}</strong> 3x time per day:
              </p>
              <ul class="text">
                <li>Early morning (6:00)</li>
                <li>Noon (12:00)</li>
                <li>Evening (18:00)</li>
              </ul>
            </div>
           
            <div v-if="subscribePeriod == 'daily'">
              <p>
                You will be receiving <strong>{{ author.name }}</strong> daily at 
                <strong>{{subscribeTime}}</strong>.
              </p>
            </div>

            <div v-if="subscribePeriod == 'weekly'">
              <p>
                You will be receiving <strong>{{ author.name }}</strong> weekly on
                <strong>{{dow[subscribeDow - 1]}}</strong> at <strong>{{subscribeTime}}</strong>.
              </p>
            </div>
          </section>

          <section v-if="subscribeStep == 3">
            <header>
              What time?
              <button-icon tabindex="0" v-on:click="goOneStepBack()"></button-icon>
            </header>
            <ul>
              <li><a href="" v-on:click.prevent="selectWhatTime('6:00', $event)">Early morning (6:00)</a></li>
              <li><a href="" v-on:click.prevent="selectWhatTime('9:00', $event)">Morning (9:00)</a></li>
              <li><a href="" v-on:click.prevent="selectWhatTime('12:00', $event)">Noon (12:00)</a></li>
              <li><a href="" v-on:click.prevent="selectWhatTime('15:00', $event)">After noon (15:00)</a></li>
              <li><a href="" v-on:click.prevent="selectWhatTime('18:00', $event)">Evening (18:00)</a></li>
              <li><a href="" v-on:click.prevent="selectWhatTime('21:00', $event)">Night (21:00)</a></li>
            </ul>
          </section>

          <section v-if="subscribeStep == 2">
            <header>
              Which day?
              <button-icon tabindex="0" v-on:click="goOneStepBack()"></button-icon>
            </header>
            <ul>
              <li><a href="" v-on:click.prevent="selectWhatDay('1', $event)">Monday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('2', $event)">Tuesday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('3', $event)">Wednesday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('4', $event)">Thursday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('5', $event)">Friday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('6', $event)">Saturday</a></li>
              <li><a href="" v-on:click.prevent="selectWhatDay('7', $event)">Sunday</a></li>
            </ul>
          </section>
        </follow-author>
      </author-detail--subscribe>

      <author-detail--editions v-if="editions.length">
        <h2>{{ author.name }}'s Editions</h2>

        <div>
          <MyEditionsItem
            v-for="edition in editions"
            :key="edition.id"
            v-bind:edition="edition"
          />
        </div>

        <button v-if="editionIds.length > 3" v-on:click="toggleEditions()">{{ !showAllEditions ? 'Show all editions' : 'Hide editions' }}</button>

      </author-detail--editions>

      <author-detail--posts v-if="posts.length">
        <h2>{{ author.name }}'s Posts</h2>

        <PostWrapper
          v-for="post in posts"
          :post="post"
          :isSubscribed="true"
          :key="post.id"
        />
      </author-detail--posts>

      <loading-spinner v-if="loadingPosts"></loading-spinner>
    </div>

  </author-detail-view>
</template>


<script>
import * as api from '@/api'

import MyEditionsItem from '@/components/MyEditionsItem'
import PostWrapper from '@/components/PostWrapper'
import { directive as onClickaway } from 'vue-clickaway'

export default {
  name: 'AuthorDetail',
  directives: {
    onClickaway,
  },
  components: {
    MyEditionsItem,
    PostWrapper
  },

  data() {
    return {
      loadingProfile: true,
      loadingPosts: true,
      author: null,
      showAllEditions: false,
      editionIds: [],
      posts: [],
      cursor: null,
      subscribePeriod: null,
      subscribeTime: null,
      subscribeDow: null,
      subscribeStep: null,
      dow: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    editions() {
      const ids = this.showAllEditions ? this.editionIds : this.editionIds.slice(0, 3)
      return ids.map(id => this.$store.getters.edition(id))
    }
  },

  methods: {
    openSubscribeWidget() {
      this.subscribeStep = 1
    },

    closeSubscribeWidget() {
      this.subscribePeriod = null
      this.subscribeTime = null
      this.subscribeDow = null
      this.subscribeStep = null
    },

    goOneStepBack() {
      if (this.subscribePeriod == 'daily') {
        this.subscribeStep = 1
      } else {
        this.subscribeStep--
      }
    },

    selectHowOften(period, ev) {
      ev.target.blur()
      this.subscribePeriod = period

      if (period == '3X') {
        this.subscribeStep = 4
        this.follow(period)  
      }
      else if (period == 'daily') {
        this.subscribeStep = 3
      }
      else if (period == 'weekly') {
        this.subscribeStep = 2
      }
    },

    selectWhatTime(time, ev) {
      ev.target.blur()
      this.subscribeTime = time
      
      if (this.subscribePeriod == 'daily') {
        this.follow('D', time)
      }
      else if (this.subscribePeriod == 'weekly') {
        this.follow('W', time, this.subscribeDow)
      }

      this.subscribeStep = 4
    },

    selectWhatDay(dow, ev) {
      ev.target.blur()
      this.subscribeDow = dow
      this.subscribeStep = 3
    },

    follow(period, time, dow) {
      // TODO split handlers
      this.$store.dispatch('invalidateTimeline')
      api.subscribeAuthor(this.author, period, time, dow).then(author => this.author)
      this.author.isSubscribed = true
    },

    unfollow(ev) {
      // TODO split handlers
      this.$store.dispatch('invalidateTimeline')
      api.unsubscribeAuthor(this.author).then(author => this.author)
      this.author.isSubscribed = false
      ev.target.blur()
    },

    toggleEditions() {
      this.showAllEditions = !this.showAllEditions
    },

    handlePostsData(resp) {
      resp.posts.forEach(post => this.posts.push(post))
      this.cursor = resp.cursor
      this.loadingPosts = false
    },

    loadMore() {
      if (this.cursor) {
        this.loadingPosts = true
        api.getAuthorPosts(this.$route.params.authorId, this.cursor).then(this.handlePostsData)
      }
    }
  },

  created() {
    api.getAuthorDetail(this.$route.params.authorId).then(resp => {
      resp.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
      this.author = resp.author
      this.editionIds = resp.editions.map(e => e.id)
      this.loadingProfile = false
    })
    api.getAuthorPosts(this.$route.params.authorId, null).then(this.handlePostsData)
  }
}
</script>

<style lang="sass">
//- AUTHOR DETAIL -//

author-detail-view
  display: block
  margin: 0 auto
  max-width: 900px

//- Header
author-detail--header
  display: block
  padding: $baseline 0

  font-family: $ff-serif
  text-align: center

  //- Author name
  h1
    margin-bottom: $baseline

    font-size: $fs-4
    line-height: $baseline * 2

  picture
    display: table
    margin: 0 auto

    img
      border-radius: 100%
      height: $baseline * 4
      width: $baseline * 4

      object-fit: cover

//- Subsribe
author-detail--subscribe
  position: relative

  display: block
  margin-bottom: $baseline

  text-align: center

  button
    +subscribe-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    margin: 0 $baseline / 2

    font-size: $fs-1

//- Editions
author-detail--editions
  display: block
  margin-bottom: $baseline

  h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

  img
    max-width: 100%

  //- wrapper for edition items
  > div
    display: flex
    flex-wrap: wrap
    margin: 0 -$baseline/4

  //- show/hide more editions
  > button
    display: table
    border-radius: $baseline
    height: $baseline * 1.25
    padding: 0 $baseline
    margin: 0 auto

    background: $c-base
    border: 0
    color: #fff

    font-family: $ff-sans
    font-size: $fs--1
    cursor: pointer

    &:hover,
    &:focus
      background: darken($c-base, 10%)

//- Posts
author-detail--posts
  display: block
  margin-bottom: $baseline

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

//- Follow Author Widget -//
follow-author
  position: absolute
  left: 50%
  top: 50px
  z-index: 1

  margin-left: -125px

  display: block
  border-radius: 5px
  width: 250px

  background: #fff
  border: 1px solid #eee
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.15)

  &::after
    bottom: 100%
    left: 50%
    border: solid transparent
    content: " "
    height: 0
    width: 0
    position: absolute
    pointer-events: none
    border-bottom-color: lighten($c-base, 30%)
    border-width: 15px
    margin-left: -15px


  //- header
  header
    position: relative

    border-radius: 5px 5px 0 0

    background: lighten($c-base, 30%)
    color: #000

    font-weight: 600
    font-size: $fs--1
    line-height: $baseline * 1.25
    text-align: center

    //-- arrow back
    button-icon 
      position: absolute
      left: 0

      width: $baseline * 1.25

      color: darken($c-base, 20%)

      cursor: pointer
      font-size: $fs--2

      &:focus,
      &:hover
        background: lighten($c-base, 15%)
        color: #000

      &::before
        content: $fa-var-arrow-left



  //- steps
  section
    text-align: left  

    p 
      padding: $baseline / 2

      font-size: $fs--2
      line-height: $baseline * 0.75

      strong
        font-weight: 600

    ul.text 
      padding: 0 $baseline/2 $baseline/2 $baseline

      font-size: $fs--2
      line-height: $baseline * 0.75 

      li
        list-style: disc

    li a
      position: relative

      display: block
      padding: 0 $baseline/2  

      color: #000

      line-height: $baseline * 1.25
      text-decoration: none

      transition: 0.15s all

      &::after
        +fa-icon()
        
        position: absolute
        right: $baseline / 2
        top: 8px

        color: darken($c-base, 20%)
        opacity: 0

        font-size: $fs--2

        content: $fa-var-arrow-right

        transition: 0.15s all

      &:hover,
      &:focus
        background: lighten($c-base, 40%)

        &::after
          opacity: 1

</style>
