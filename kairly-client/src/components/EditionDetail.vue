<template>
  <app-layout>
    <edition-detail-view>

      <edition-detail--header v-if="!loading">
        <h1>{{ edition.title }}</h1>

        <edition-detail--subscribe v-if="!loading">
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
        </edition-detail--subscribe>
      </edition-detail--header>

      <div v-if="!loading">
        <edition-detail--info>
          <ul>
            <li class="periodicity">{{ edition.periodicity.frequency }} {{ edition.periodicity.time }} {{ edition.periodicity.dow }}</li>

            <li>#{{ edition.issues }}</li>

            <li>{{ edition.likes }} readers</li>

            <li>10 CZK / month</li>
          </ul>
        </edition-detail--info>

        <edition-detail--description>
          <section>
            <p>
              {{ edition.description }}
            </p>

            <footer>
              <router-link :to="{name: 'author', params: {author: edition.editor.id}}">
                <img :src="edition.editor.picture" :alt="edition.editor.name"/>
                {{ edition.editor.name }}
              </router-link>
            </footer>
          </section>

          <picture>
            <img :src="edition.picture" :alt="edition.title"/>
          </picture>
        </edition-detail--description>
      </div>

      <edition-detail--last-edition v-if="issue">
        <Issue :issue="issue" :subscription="edition.subscription" />
      </edition-detail--last-edition>
    </edition-detail-view>
  </app-layout>
</template>


<script>
import { mapGetters, mapMutations } from 'vuex'

import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'
import Issue from '@/components/IssueWrapper'
import EditionBacklog from '@/components/editor/EditionBacklog'

export default {
  name: 'EditionDetail',

  metaInfo() {
      return {
        title: this.edition ? this.edition.title : undefined
      }
  },

  components: {
    AppLayout,
    Issue,
    EditionBacklog
  },

  data() {
    return {
      loading: true,
      edition: null,
      issue: null,
    }
  },

  computed: {
    isEditor() {
      if (this.edition) {
        const author = this.edition.editor
        return this.user.id === author.id
      } else {
        return false
      }
    },

    isSubscribed() {
      return this.edition.fullName in this.$store.state.subscriptions.editions
    },

    ...mapGetters(['user'])
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', this.edition.fullName)
      document.activeElement.blur()
    },

    unsubscribe(ev) {
      this.$store.dispatch('unsubscribe', this.edition.fullName)
      document.activeElement.blur()
    },

    ...mapMutations(['show404'])
  },

  created() {
    const { author, edition } = this.$route.params
    api.getEditionDetail(`${author}/${edition}`).then(resp => {
      this.edition = resp.edition
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
edition-detail-view
  position: relative

  display: block
  margin: 0 auto
  max-width: 900px

//- Header
edition-detail--header
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
edition-detail--subscribe
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


edition-detail--info
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
edition-detail--description
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


edition-detail--last-edition
  display: block
  padding-top: $baseline * 2
</style>
