<template>
  <PostBase :post="post">
    <template slot="author">
      <picture>
        <span class="external-link"></span>
      </picture>

      <h3>External article</h3>

      <time>
        {{ post.time | moment('calendar') }}
      </time>
    </template>

    <div class="post-link-view">
      <h2>
        <a :href="post.source" target="_blank">{{ post.content.title }}</a>
      </h2>

      <div>
        <picture v-if="post.content.attachments && post.content.attachments.image">
          <img :src="post.content.attachments.image"/>
        </picture>

        <p>{{ post.content.perex }}</p>

        <div class="post-link--continue-reading">
          <a :href="post.source" target="_blank">{{ $t('Read article') }}</a>
        </div>
      </div>
    </div>
    <template slot="controls"><slot name="controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'post-link',

  props: ["post", "isSubscribed"],

  components: { PostBase }
}
</script>

<style lang="sass">
@import './styles/components/article-perex'

post-component picture .external-link
  display: block
  border-radius: 100%
  height: $baseline * 1.5
  margin-right: $baseline / 2
  width: $baseline * 1.5

  background: #eee

  line-height: $baseline * 1.5
  text-align: center

  &::before
    @extend .fas
    content: fa-content($fa-var-external-link-square-alt)

.post-link-view
  font-family: $ff-serif

  //- title
  > h2
    display: block
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600
    line-height: 1.58
    word-break: break-word

    @media (max-width: $mobile)
      font-size: $fs-0

    a
      color: #000

  > div
    column-count: 2
    column-rule: 1px dotted #ddd
    column-gap: $baseline
    display: block

    line-height: 1.58
    hyphens: auto

    @media (max-width: $mobile)
      column-gap: $baseline / 2

      font-size: 15px
      line-height: 1.58

  //- image
  img
    width: 100%

//- continue reading
.post-link--continue-reading
  display: block

  color: #999

  font-family: $ff-sans
  font-size: $fs--1
  text-align: center

  a[href]
    display: table
    border-radius: 15px
    clear: both
    margin: $baseline / 2 auto 0 auto
    padding: 0 $baseline / 2

    border: 1px solid transparent
    color: $c-base

    font-size: $fs--1
    line-height: 1.58
    text-transform: uppercase
    text-decoration: none

    &:focus,
    &:hover
      background: $c-base
      color: #fff
</style>