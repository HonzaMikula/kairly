<template>
  <app-layout>
    <post-detail role="article">
      <loading-spinner v-if="!post"></loading-spinner>

      <div v-if="post">
        <post-detail--back-button
          v-tooltip.right="'Back to Browsing Editions'"
          v-on:click="$router.go(-1)">
        </post-detail--back-button>

        <post-detail--read-later
          v-tooltip.right="'Read Later'">
        </post-detail--read-later>

        <main>
          <post-detail--header>
            <router-link :to="{name: 'author', params: {authorId: post.author.id}}">
              <img :src="post.author.picture" :alt="post.author.name"/>
              {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
            </router-link>

            <button-icon class="read-later" v-tooltip.top="'Read Later'"></button-icon>
          </post-detail--header>

          <post-detail--title>
            <h1>{{post.content.title}}</h1>
          </post-detail--title>

          <post-detail--content v-html="post.content.perex"></post-detail--content>

          <post-detail--continue-reading id="continue" v-if="post.content.content">
            continue reading
          </post-detail--continue-reading>

          <post-detail--content v-html="post.content.content"></post-detail--content>

          <post-detail--footer>
            <button-icon class="recommend">Recommend</button-icon>
            <button-icon class="share">Share</button-icon>
            <button-icon class="consider-for-edition">Consider for Edition</button-icon>
          </post-detail--footer>

          <post-detail--author>
            <picture>
              <router-link :to="{name: 'author', params: {authorId: post.author.id}}">
                <img :src="post.author.picture" :alt="post.author.name"/>
              </router-link>
            </picture>

            <h3>
              <router-link :to="{name: 'author', params: {authorId: post.author.id}}">
                {{post.author.name}}<span v-if="post.author.medium">, {{post.author.medium}}</span>
              </router-link>
            </h3>

            <p>{{post.author.bio}}</p>
          </post-detail--author>
        </main>
      </div>
    </post-detail>
  </app-layout>
</template>

<script>
import request from 'superagent'
import * as api from '@/api'

import AppLayout from '@/components/layout/AppLayout'

export default {
  name: 'PostDetailPage', // can't use PostDetail because post-detail is already used

  components: {
    AppLayout
  },

  data() {
    return {
      post: null
    }
  },

  created() {
    api.getPost(this.$route.params.postId).then(post => this.post = post)
  },

  updated() {
    // TODO dangerous if more component properties exists and updated called more
    // then once
    if (this.$route.hash) {
      const anchor = document.querySelector(this.$route.hash)
      if (anchor) {
        anchor.scrollIntoView(true)
      }
    }
  }
}
</script>

<style lang="sass">
//- POST DETAIL -//

post-detail
  position: relative

  display: block
  padding: 0 $baseline/2
  min-height: calc(100vh - (#{$baseline} * 2))

  background: #fff

  //- wrapper
  > div
    padding: $baseline 0
    margin: 0 auto
    max-width: 900px

  main
    margin: 0 auto
    max-width: 700px


//- Back Button
post-detail--back-button
  position: sticky
  left: $baseline
  top: $baseline

  display: inline-block
  border-radius: 100%
  height: $baseline * 2
  width: $baseline * 2

  background: #eee

  cursor: pointer
  font-size: $fs-1
  line-height: $baseline * 2
  text-align: center

  &:focus,
  &:hover
    background: $c-base
    color: #fff

  &::before
    +fa-icon()

    content: $fa-var-arrow-left

  @media (max-width: $mobile)
    position: static


//- Read Later Button
post-detail--read-later
  position: sticky
  top: $baseline

  display: inline-block
  border-radius: 100%
  height: $baseline * 2
  float: right
  width: $baseline * 2

  background: #eee

  cursor: pointer
  font-size: $fs-1
  line-height: $baseline * 2
  text-align: center

  &:focus,
  &:hover
    background: $c-base
    color: #fff

  &::before
    +fa-icon()

    content: $fa-var-bookmark

  @media (max-width: $mobile)
    position: static


//- Header
post-detail--header
  display: table
  margin-bottom: $baseline
  margin-top: -$baseline * 2
  width: 100%

  a
    color: #555

    line-height: $baseline * 1.25

    //- author picture
    img
      border-radius: 100%
      float: left
      height: $baseline * 1.25
      margin-right: $baseline / 4
      width: $baseline * 1.25

      object-fit: cover


//- Title
post-detail--title
  display: block
  margin-bottom: $baseline

  font-family: $ff-serif
  font-size: $fs-3
  font-weight: 600
  line-height: $baseline * 1.25

  @media (max-width: $mobile)
    font-size: $fs-2
    line-height: $baseline


//- Continue Reading
post-detail--continue-reading
  position: relative

  display: block
  margin: $baseline*1.5 0

  color: #999

  font-family: $ff-serif
  font-size: $fs-1
  font-weight: 600
  text-align: center

  &::after,
  &::before
    position: absolute
    top: $baseline / 2

    height: 1px
    width: 30%

    background: #eee

    content: ''

  &::before
    left: 0

  &::after
    right: 0


//- Content
post-detail--content,
post-detail--perex
  display: block

  font-family: $ff-serif
  font-size: $fs-1
  line-height: $baseline * 1.25

  @media (max-width: $mobile)
    font-size: $fs-0
    line-height: $baseline

  //- title
  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  //- Headings
  h2, h3, h4, h5, h6
    margin-bottom: $baseline

    font-weight: 600

  //- Paragraph
  p
    margin-bottom: $baseline

  //- Strong
  strong, b
    font-weight: 600

  //- Italic
  em, i
    font-style: italic

  //- Lists
  ul
    margin: 0 0 $baseline $baseline

  //-- bullet points
  ul li
    margin-left: $baseline
    list-style: disc outside

  //-- ordered list
  ol li
    margin-left: $baseline
    list-style: decimal outside

  //- Image
  img
    height: auto
    max-width: 100%

  //- Video
  video
    height: auto
    max-width: 100%

  //- Link
  a[href]
    color: $c-base

  //-- code inline
  code
    background: #fafafa
    font-family: "courier new", courier, monospace
    font-size: $fs--1

  //-- code block
  pre
    overflow: auto

    background: #fafafa
    border: 1px solid #eee

    font-family: "courier new", courier, monospace
    font-size: $fs--2


  //-- pictures
  figure
    margin-bottom: $baseline

    text-align: center

    figcaption, p
      color: #999

      font-family: $ff-sans
      font-size: $fs--2
      line-height: $baseline * 0.9


//- Post Footer
post-detail--footer
  display: block
  padding-bottom: $baseline / 2
  margin-bottom: $baseline / 2

  border-bottom: 1px solid #eee

  button-icon
    border-radius: 5px
    display: inline-block
    height: $baseline * 1.25
    margin-right: $baseline / 2
    padding: 0 $baseline/4

    background: #eee

    cursor: pointer
    font-size: $fs--2
    line-height: $baseline * 1.25
    vertical-align: middle

    &::before
      position: relative
      top: -1px

      margin-right: $baseline / 4
      vertical-align: middle

      font-size: $fs-1

    &:focus,
    &:hover
      background: #bbb
      color: #000

//- Post Author
post-detail--author
  display: grid
  grid-template-areas: "post-detail-author-image post-detail-author-name" "post-detail-author-image post-detail-author-bio"
  grid-template-columns: $baseline*3 auto
  grid-template-rows: $baseline auto
  grid-gap: 0 $baseline/2

  //- picture
  picture
    grid-area: post-detail-author-image

    img
      border-radius: 100%
      height: $baseline * 3
      width: $baseline * 3

      object-fit: cover

  //- name
  h3
    grid-area: post-detail-author-name

    font-size: $fs-0
    font-weight: 600

    a
      color: #000

  //- bio
  p
    grid-area: post-detail-author-bio

    font-size: $fs--1
</style>
