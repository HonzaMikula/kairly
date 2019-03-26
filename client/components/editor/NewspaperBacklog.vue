<template>
  <div class="newspaper-backlog-view">

    <div class="newspaper-backlog--info">
      <div>
        <p>
          {{ $t('Issue') }} <strong>#{{newspaper.issues + 1}}</strong>
          {{ $t('will be automatically published in') }}
          <strong :title="newspaper.nextRelease">{{timeFrom(newspaper.nextRelease)}}</strong>
        </p>

        <p class="newspaper-backlog--info--profit">
          <strong
            @click="openProfitDropdown = !openProfitDropdown"
            v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
            :title="$t('Revenue - Cost = Profit')">
            {{ fmtPrice(revenuePerIssue) }}
            -
            {{ fmtPrice(currentIssueCost) }}
            =
            {{ fmtPrice(profitPerIssue) }} Kč
          </strong>
        </p>

        <div
          v-if="openProfitDropdown"
          v-on-clickaway="() => openProfitDropdown = false"
          class="newspaper-backlog--info--profit-dropdown">

          <table>
            <thead>
              <tr>
                <th>{{ $t('Current Issue') }}</th>
                <th>{{ $t('Per subscriber') }}</th>
                <th>{{ $t('For {subscribers} subscribers', {subscribers: newspaper.likes}) }}</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <th>{{ $t('Avg. revenue per issue') }}</th>
                <td>{{ fmtPrice(revenuePerIssue) }} Kč</td>
                <td>{{ fmtPrice(revenuePerIssue * newspaper.likes) }} Kč</td>
              </tr>
              <tr>
                <th>{{ $t('Cost of current issue') }}</th>
                <td>{{ fmtPrice(currentIssueCost) }} Kč</td>
                <td>{{ fmtPrice(currentIssueCost * newspaper.likes) }} Kč</td>
              </tr>
              <tr class="profit">
                <th>{{ $t('Profit from current issue') }}</th>
                <td>{{ fmtPrice(profitPerIssue) }} Kč</td>
                <td>{{ fmtPrice(profitPerIssue * newspaper.likes) }} Kč</td>
              </tr>
            </tbody>

            <thead>
              <tr>
                <th>{{ $t('Total for this month') }}</th>
                <th>{{ $t('Per subscriber') }}</th>
                <th>{{ $t('For {subscribers} subscribers', {subscribers: newspaper.likes}) }}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th>{{ $t('Total revenues') }}</th>
                <td>{{ fmtPrice(newspaper.price) }} Kč</td>
                <td>{{ fmtPrice(newspaper.price * newspaper.likes) }} Kč</td>
              </tr>

              <tr>
                <th>{{ $t('Number of previous issues') }}</th>
                <td colspan="2">{{ currentMonth.priorIssues }}</td>
              </tr>

              <tr>
                <th>{{ $t('Cost of previous issues') }}</th>
                <td>{{ fmtPrice(currentMonth.priorIssuesCost) }} Kč</td>
                <td>{{ fmtPrice(currentMonth.priorIssuesCost * newspaper.likes) }} Kč</td>
              </tr>

              <tr>
                <th>{{ $t('Number of remaining issues') }}</th>
                <td colspan="2">{{ currentMonth.upcommingIssues }}</td>
              </tr>

              <tr class="profit">
                <th>{{ $t('Remaining profit') }}</th>
                <td>{{ fmtPrice(profit) }} Kč</td>
                <td>{{ fmtPrice(profit * newspaper.likes) }} Kč</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <p v-html="$t('<strong>{backlogLength} posts</strong> are considered', {backlogLength: backlog.length})" />
      </div>
    </div>

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

        <div
          v-for="post in backlog"
          :key="post.id"
          class="backlog-post"
        >
          <header>
            <picture>
              <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
                <img :src="post.author.picture" :alt="post.author.name" />
              </nuxt-link>
            </picture>

            <h3>
              <nuxt-link :to="{name: 'author', params: {author: post.author.id}}">
                {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
              </nuxt-link>
            </h3>

            <time>
              {{ post.time | moment('calendar') }}
              •
              {{ post.timeRead }} {{ $t('read') }}
              •
              {{ post.price }} Kč
            </time>

            <section>
              <button @click="publish(post)">{{ $t('Publish') }}</button>

              <button-icon
                class="remove"
                role="button"
                :title="$t('Remove post from considaration')"
                v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
                tabindex="0"
                @click.prevent="removePost(post)">
              </button-icon>
            </section>

          </header>

          <template v-if="post.type == 'tweet'">
            <p v-html="post.content.content"></p>
          </template>

          <template v-else>
            <h2><nuxt-link :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link></h2>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'
import moment from 'moment'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'NewspaperBacklog',

  components: {
    PostWrapper
  },

  directives: {
    onClickaway
  },

  props: {
    newspaper: Object,
    backlog: Array,
    published: Array,
    currentMonth: Object,
  },

  data() {
    return {
      openProfitDropdown: false
    }
  },

  computed: {
    currentIssueCost() {
      return this.published.map(item => item.price).reduce((prev, next) => parseFloat(prev) + parseFloat(next), 0)
    },

    cost() {
      return parseFloat(this.currentMonth.priorIssuesCost) + this.currentIssueCost
    },

    profit() {
      return parseFloat(this.newspaper.price) - this.cost
    },

    revenuePerIssue() {
      const totalIssues = this.currentMonth.priorIssues + this.currentMonth.upcommingIssues
      return parseFloat(this.newspaper.price) / totalIssues
    },

    profitPerIssue() {
      return this.revenuePerIssue - this.currentIssueCost
    }
  },

  methods: {
    timeFrom(dt) {
      return moment(dt).from()
    },

    fmtPrice(value) {
      if (value === null) {
        return ''
      }
      if (typeof value.toFixed === 'function') {
        return value.toFixed(2)
      }
      return value
    },

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


//- Info when release go out
.newspaper-backlog--info
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

  > div
    position: relative

    display: flex

    //- report button opening dropdown
    button-icon.report
      &::before
        +fa-icon()
        @extend .fas

        content: fa-content($fa-var-chart-bar)

    p:first-child
      margin-right: auto

p.newspaper-backlog--info--profit
  strong
    margin-right: $baseline / 2

    color: $c-base

    cursor: pointer

    &:hover,
    &:focus
      darken($c-base, 10%)

//- Detail report dropdown
.newspaper-backlog--info--profit-dropdown
  position: absolute
  right: 0
  top: $baseline
  z-index: 1

  padding: $baseline/4 $baseline/2

  background: #fff
  border: 1px solid #eee
  +box-shadow

  //- general table
  td, th
    padding: $baseline/4 $baseline/2 $baseline/4 0

    font-family: $ff-sans
    text-align: left

  th
    font-weight: 600

  //- header
  thead:last-of-type th
    padding-top: $baseline

  //- body
  tbody th
    font-weight: 400

  tbody td
    text-align: right

    &[colspan]
      text-align: center

      &::before,
      &::after
        content: ' ~ '

  //- profit
  .profit th,
  .profit td
    border-top: 1px solid #555
    font-weight: 600



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

        font-size: $fs--1
        line-height: $baseline * 0.75

        a
          color: $c-base


      //-- date of publication
      time
        grid-area: info
        width: 100%

        color: #999

        font-size: $fs--1
        line-height: $baseline * 0.75

      //-- controls
      section
        > button
          +button(primary, small)

        button-icon
          display: inline-block
          border-radius: 100%
          width: $baseline

          background: #eee

          text-align: center

          transition: 0.15s background

          &:focus,
          &:hover
            background: #ddd

</style>
