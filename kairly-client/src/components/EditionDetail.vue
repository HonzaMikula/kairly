<template>
  <edition-detail-view>

    <div v-if="!loading">
      <edition-detail--header>
        <h1>{{ edition.title }}</h1>

        <router-link :to="{name: 'author', params: {authorId: edition.editor.id}}">
          <img :src="edition.editor.picture" :alt="edition.editor.name"/>
          {{ edition.editor.name }}
        </router-link>
      </edition-detail--header>

      <edition-detail--description>
        <p>
          {{ edition.description }}
        </p>

        <div>
          <div>
            <h3>Periodicity</h3>
            <p>
              {{ edition.periodicity.frequency }}
              {{ edition.periodicity.time }}
              {{ edition.periodicity.dow }}
            </p>
          </div>

          <div>
            <h3>Issues</h3>
            <p>{{ edition.issues }}</p>
          </div>

          <div>
            <h3>Subscribers</h3>
            <p>{{ edition.likes }}</p>
          </div>
        </div>
      </edition-detail--description>

      <edition-detail--subscribe>
        <button
          v-bind:class="{ 'is-subscribed': edition.subscription }"
          v-on:click="subscribe($event)"
        >{{ edition.subscription ? 'Subscribed' : 'Subscribe Edition'}}</button>

        <p>10 CZK per month</p>
      </edition-detail--subscribe>

      <edition-detail--picture>
        <img :src="edition.picture" :alt="edition.title"/>
      </edition-detail--picture>
    </div>

    <div v-if="isEditor">
      <a href="#" @click.prevent="confirmDeleteEdition">Delete edition</a>
    </div>

    <edition-backlog v-if="isEditor" :edition="edition" />

    <edition-detail--last-edition v-if="issue">
      <h2><span>Check the Last Issue</span></h2>

      <Issue :issue="issue" :subscription="edition.subscription" />
    </edition-detail--last-edition>
  </edition-detail-view>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import * as api from '@/api'

import Issue from '@/components/IssueWrapper'
import EditionBacklog from '@/components/editor/EditionBacklog'



export default {
  name: 'EditionDetail',

  components: {
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
        return this.user.author && this.user.author.id === author.id
      } else {
        return false
      }
    },

    ...mapState({
      user: state => state.user
    }),
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', {
        edition: this.edition,
        value: !this.edition.subscription
      })
      this.edition.subscription = !this.edition.subscription
      ev.target.blur()
    },

    confirmDeleteEdition() {
      if (window.confirm("Are you sure?")) {
        this.deleteEdition(this.edition)
      }
    },

    ...mapActions(['deleteEdition'])
  },

  created() {
    api.getEditionDetail(this.$route.params.editionId).then(resp => {
      this.edition = resp.edition
      this.issue = resp.issue
      this.loading = false
    })
  }
}
</script>

<style lang="sass">
edition-detail-view
  display: block
  margin: 0 auto
  max-width: 900px

  > div
    display: grid
    grid-template-areas: "edition-detail-header edition-detail-header" "edition-detail-description edition-detail-picture" "edition-detail-subscribe edition-detail-picture"
    grid-template-columns: 50% 50%
    grid-template-rows: auto
    padding: $baseline $baseline 0 $baseline

    @media (max-width: $mobile)
      grid-template-areas: "edition-detail-header" "edition-detail-picture" "edition-detail-description" "edition-detail-subscribe"
      grid-template-columns: 100%


//- Header
edition-detail--header
  grid-area: edition-detail-header
  margin-bottom: $baseline

  font-family: $ff-serif

  //- Title
  h1
    margin-bottom: $baseline / 2

    font-size: $fs-4
    line-height: $baseline * 2
    text-align: center

  //- Editor
  > a
    display: table
    margin: 0 auto

    color: #999

    font-size: $fs-1

    img
      border-radius: 100%
      height: $baseline * 1.5
      width: $baseline * 1.5

      object-fit: cover
      vertical-align: middle


//- Editorial Intro
edition-detail--description
  grid-area: edition-detail-description

  font-family: $ff-serif

  p
    margin-bottom: $baseline

  > div
    display: flex

  > div > div
    margin-right: $baseline

    &:last-of-type
      margin-right: 0

  h3
    font-size: $fs--1
    text-transform: uppercase

  h3 + p
    margin-bottom: $baseline / 2

    font-weight: 600


//- Subscribe
edition-detail--subscribe
  grid-area: edition-detail-subscribe
  justify-self: center
  margin-top: $baseline

  button
    +subscribe-button

    border-radius: $baseline * 0.75
    height: $baseline * 1.5

    font-size: $fs-1

  button + p
    color: #777

    font-size: $fs--2
    text-align: center


//- Edition Picture
edition-detail--picture
  grid-area: edition-detail-picture

  img
    max-width: 100%


//- Last Edition
edition-detail--last-edition
  display: block
  margin-top: $baseline

  > h2
    position: relative

    margin-bottom: $baseline

    font-family: $ff-serif
    text-align: center
    text-transform: uppercase

    span
      position: relative
      z-index: 1

      padding: 0 $baseline/2

      background: #fafafa

    &::before
      position: absolute
      left: 0
      top: $baseline / 2

      height: 1px
      width: 100%

      background: #eee

      content: ''
</style>
