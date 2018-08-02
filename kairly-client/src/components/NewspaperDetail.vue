<template>
  <app-layout>
    <newspaper-detail-view>

      <newspaper-detail--header v-if="!loading">
        <h1>{{ newspaper.title }}</h1>

        <newspaper-detail--subscribe v-if="!loading">
          <button
            v-if="isSubscribed"
            class="is-subscribed"
            @click="unsubscribe($event)">
            <span class="default">Subscribed</span>
            <span class="on-hover">Unsubscribe</span>
          </button>

          <button
            v-else
            class="to-subscribe"
            @click="subscribe($event)">
            Subscribe
          </button>

          <p>10 CZK per month</p>
        </newspaper-detail--subscribe>
      </newspaper-detail--header>

      <div v-if="!loading">
        <newspaper-detail--info>
          <ul>
            <li class="periodicity">{{ newspaper.periodicity.frequency }} {{ newspaper.periodicity.time }} {{ newspaper.periodicity.dow }}</li>

            <li>#{{ newspaper.issues }}</li>

            <li>{{ newspaper.likes }} readers</li>

            <li>10 CZK / month</li>
          </ul>
        </newspaper-detail--info>

        <newspaper-detail--description>
          <section>
            <p>
              {{ newspaper.description }}
            </p>

            <footer>
              <router-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
                <img :src="newspaper.editor.picture" :alt="newspaper.editor.name"/>
                {{ newspaper.editor.name }}
              </router-link>
            </footer>
          </section>

          <picture>
            <img :src="newspaper.picture" :alt="newspaper.title"/>
          </picture>
        </newspaper-detail--description>
      </div>

      <newspaper-detail--last-newspaper v-if="issue">
        <Issue :issue="issue" :subscription="newspaper.subscription" />
      </newspaper-detail--last-newspaper>

      <newspaper-detail--empty-newspaper v-else>
        <h2>No issue yet</h2>

        <p>
          Subscribe the newspaper and once it's published, we will show you on your timeline.
        </p>
      </newspaper-detail--empty-newspaper>
    </newspaper-detail-view>
  </app-layout>
</template>


<script>
import { mapGetters, mapMutations } from 'vuex'

import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'
import NewspaperBacklog from '@/components/editor/NewspaperBacklog'

export default {
  name: 'NewspaperDetail',

  metaInfo() {
      return {
        title: this.newspaper ? this.newspaper.title : undefined
      }
  },

  components: {
    AppLayout,
    Issue,
    NewspaperBacklog
  },

  data() {
    return {
      loading: true,
      newspaper: null,
      issue: null,
    }
  },

  computed: {
    isEditor() {
      if (this.newspaper) {
        const author = this.newspaper.editor
        return this.user.id === author.id
      } else {
        return false
      }
    },

    isSubscribed() {
      return this.newspaper.fullName in this.$store.state.subscriptions.newspapers
    },

    ...mapGetters(['user'])
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', this.newspaper.fullName)
      document.activeElement.blur()
    },

    unsubscribe(ev) {
      this.$store.dispatch('unsubscribe', this.newspaper.fullName)
      document.activeElement.blur()
    },

    ...mapMutations(['show404'])
  },

  created() {
    const { author, newspaper } = this.$route.params
    api.getNewspaperDetail(`${author}/${newspaper}`).then(resp => {
      this.newspaper = resp.newspaper
      this.issue = resp.issue
      this.loading = false
    }).catch(err => {
      if (err.status == 404) {
        this.show404()
      } else {
        return Promise.reject(err)
      }
    })
  }
}
</script>

<style lang="sass">
newspaper-detail-view
  position: relative

  display: block
  margin: 0 auto
  max-width: 900px

//- Header
newspaper-detail--header
  position: sticky
  top: -1px
  z-index: 1

  display: block
  padding: $baseline/4 $baseline
  margin: $baseline*0.75 0
  overflow: hidden

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: $mobile)
    position: static
    padding-bottom: 0
    margin: 0

  //- Title
  h1
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center
    text-shadow: 0 0 5px #fafafa

    @media (max-width: $mobile)
      font-size: $fs-3

//- Subscribe
newspaper-detail--subscribe
  position: absolute
  right: 0
  top: 0

  display: block
  padding: $baseline / 4

  backdrop-filter: blur(10px)

  @media (max-width: $mobile)
    position: static
    text-align: center

  button.is-subscribed
    +subscribed-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    width: 150px

    line-height: $baseline * 1.5

    .on-hover
      display: none

    &:hover,
    &:focus
      .on-hover
        display: block

      .default
        display: none

  button.to-subscribe
    +subscribe-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    width: 150px

    line-height: $baseline * 1.5



  button + p
    color: #777

    font-size: $fs--2
    line-height: $baseline * 0.8
    text-align: center


newspaper-detail--info
  display: block
  padding: $baseline/4 0

  border-bottom: 1px solid #ddd
  border-top: 1px solid #ddd

  .periodicity
    text-transform: capitalize

  ul
    display: table
    margin: 0 auto

    @media (max-width: $mobile)
      padding: 0 $baseline/4

  li
    display: inline-block

    font-size: $fs--1
    font-family: $ff-serif
    vertical-align: middle

    &::after
      display: inline-block
      padding: 0 $baseline/2

      content: '•'

      @media (max-width: $mobile)
        padding: 0 $baseline/4

    &:last-of-type::after
      display: none

  //- Editor
  a
    color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: middle


//- Editorial Intro
newspaper-detail--description
  display: grid
  grid-template-columns: 1fr 2fr
  grid-column-gap: $baseline
  grid-template-rows: auto
  margin-top: $baseline

  font-family: $ff-serif

  @media (max-width: $mobile)
    grid-template-columns: 1fr
    grid-row-gap: $baseline / 2
    padding: $baseline / 4
    margin-top: 0

  h3
    font-weight: 600

  p
    text-align: justify
    text-indent: $baseline

  footer
    margin-top: $baseline / 2

    font-weight: 600
    text-align: right

    a
      color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: middle

  picture
    height: 100%

    img
      height: 100%
      min-height: 250px
      max-height: 100%
      width: 100%
      object-fit: cover


newspaper-detail--last-newspaper
  display: block
  padding-top: $baseline * 2

newspaper-detail--empty-newspaper
  display: block
  margin-top: $baseline * 2
  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  h2
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600
</style>
