<template>
  <post :post="post">
    <timeline-post--newspaper>
      <h2><router-link :to="{ name: 'post', params: { postId: post.id }}">{{ post.content.title }}</router-link></h2>
      <timeline-post--newspaper--content>
        <div v-html="post.content.content"></div>
        <timeline-post--continue-reading v-if="post.timeRead && post.timeRead !='0 min'">
          <div v-if="isSubscribed">
            <router-link :to="{ name: 'post', params: { postId: post.id }, hash: '#continue'}">Continue reading</router-link>
          </div>
          <div v-else>
            Subscribe edition to continue reading
          </div>
          ({{ post.timeRead }} read)
        </timeline-post--continue-reading>
      </timeline-post--newspaper--content>
    </timeline-post--newspaper>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-newspaper',
  props: ["post", "isSubscribed"],
  components: { post }
}
</script>


<style lang="sass">
timeline-post--newspaper
  font-family: $ff-serif

  //- Title
  > h2
    display: block
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600

    a
      color: #000
      text-decoration: none

  a
    color: $c-base

    &:hover,
    &:focus
      text-decoration: none

//- Content
timeline-post--newspaper--content
  position: relative

  column-count: 3
  column-rule: 1px dotted #ddd
  column-gap: $baseline
  display: block

  line-height: $baseline * 0.9
  text-align: justify
  hyphens: auto

  @media (max-width: $mobile)
    column-count: 2


  //-- heading
  h1, h2, h3, h4, h5, h6
    margin: $baseline / 4 0
    font-weight: 600

    break-after: avoid-column

  //-- paragraph
  p
    text-indent: $baseline

  //-- illustration image
  img
    display: block
    margin: $baseline / 4 auto
    height: auto
    max-height: 200px
    max-width: 100%

  //- Video
  video
    height: auto
    max-width: 100%

  //-- link
  a[href]
    text-decoration: none

  //-- strong
  strong, b
    font-weight: 600

  //-- italic
  em, i
    font-style: italic

  //-- bullet points
  ul li
    margin-left: $baseline
    list-style: disc outside

  //-- ordered list
  ol li
    margin-left: $baseline
    list-style: decimal outside

  //-- horizontal line
  hr
    border: 0
    height: 1px
    background: #ddd

  //-- quotes
  blockquote
    margin: ($baseline / 4 - 2rem) 0
    padding: $baseline / 4 0

    border-bottom: 1px solid #eee
    border-top: 1px solid #eee
    color: #999

    font-size: $fs-1

    p
      text-indent: 0

      &::before
        content: "„"

      &::after
        content: "“"

  //-- cite
  cite
    display: block
    margin: ($baseline / 4 - 2rem) 0
    padding: $baseline / 4 0

    border-bottom: 1px solid #eee
    border-top: 1px solid #eee
    color: #999

    font-size: $fs-1
    text-indent: 0

    &::before
      content: "„"

    &::after
      content: "“"

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
    text-align: center

    figcaption, p
      color: #999

      font-family: $ff-sans
      font-size: $fs--2
      line-height: $baseline * 0.9


//- Continue Reading
timeline-post--continue-reading
  display: block

  color: #999

  font-family: $ff-sans
  font-size: $fs--2
  text-align: center

  a
    display: table
    border-radius: 15px
    clear: both
    margin: $baseline / 2 auto 0 auto
    padding: 0 $baseline / 2

    border: 1px solid transparent

    font-size: $fs--2
    line-height: $baseline
    text-transform: uppercase

    &:focus,
    &:hover
      background: $c-base
      color: #fff

</style>
