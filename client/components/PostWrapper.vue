<template>
  <section
    class="normal-post">
    <component
      :is="postType"
      class="post-content"
      :post="post"
      :isSubscribed="isSubscribed"
    >
      <template #author>
        <slot name="author"></slot>
      </template>

      <template #extended-controls>
        <slot name="extended-controls"></slot>
      </template>

      <template #controls>
        <slot name="controls"></slot>
      </template>
    </component>

    <!--slot name="editorial">
      <aside>
      <component
        v-if="editorial"
        :is="'editorial-' + editorial.type"
        :editorial="editorial"
      />
      </aside>
    </slot-->
  </section>
</template>

<script>
import PostArticle from '@/components/posts/PostArticle'
import PostComment from '@/components/posts/PostComment'
import PostLink from '@/components/posts/PostLink'
import PostTweet from '@/components/posts/PostTweet'
import PostPicture from '@/components/posts/PostPicture'
import PostVideo from '@/components/posts/PostVideo'
import PostRecommendations from '@/components/posts/PostRecommendations'

//import EditorialTweets from '@/components/posts/EditorialTweets'
//import EditorialArticle from '@/components/posts/EditorialArticle'

export default {
  name: 'PostWrapper',
  props: {
    post: [Object, Array] ,
    isSubscribed: Boolean,
  },

  components: {
    PostArticle,
    PostComment,
    PostLink,
    PostTweet,
    PostPicture,
    PostVideo,
    PostRecommendations,
    //EditorialTweets,
    //EditorialArticle,
  },

  computed: {
    // basePost() {
    //   if (Array.isArray(this.post)) {
    //     const col = this.post[0] === 'cols-2-1' ? this.post[1] : this.post[2]
    //     return col[0]
    //   }
    //   return this.post
    // },

    // editorial() {
    //   if (Array.isArray(this.post)) {
    //     const col = this.post[0] === 'cols-2-1' ? this.post[2] : this.post[1]
    //     const posts = col.slice(1)
    //     const first = posts[0]
    //     const data = {
    //       'author': first.type === 'newspaper' ? first.author : null,
    //       'type': first.type === 'newspaper' ? 'article' : 'tweets',
    //       'position': this.post[0] === 'cols-2-1' ? 'right': 'left'
    //     }
    //     if (data.type === 'tweets') {
    //       data.tweets = posts
    //     } else {
    //       data.title = first.title
    //       data.content = first.content
    //     }
    //     return data
    //   }
    //   return null
    // },
    //- TEMP hack - we can get rid of it after migration
    postType() {
      function map_type(t) {
        if (t === 'newspaper') {
          return 'post-article' // TODO: back to 'article'
        } else {
          return 'post-' + t
        }
      }

      // if (Array.isArray(this.post)) {
      //   if (this.post[0] === 'cols-2-1') {
      //     return map_type(this.post[1][0].type)
      //   } else {
      //     return map_type(this.post[2][0].type)
      //   }
      // }
      // if (this.editorial == 'article' || this.editorial == 'tweet') {
      //   return 'editorial'
      // }
      return map_type(this.post.type)
    }
  }
}
</script>

<style lang="sass">
.editorial-post
  position: relative

  display: grid
  grid-template-columns: 1fr 1fr 1fr
  margin-bottom: $baseline / 2

  background: #F2ECEC
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  @media (max-width: $mobile)
    grid-template-columns: calc(100vw - (#{$baseline} * 1.5)) 60vw

    overflow: auto
    scroll-behavior: smooth
    -webkit-overflow-scrolling: touch

    &.is-before
      grid-template-columns: 60vw calc(100vw - (#{$baseline} * 1.5))

  > aside
    display: flex
    flex-direction: column
    justify-content: center

  > aside > div
    @media (max-width: $mobile)
      position: absolute
      height: 100%
      width: 100%
      overflow-y: auto

  //- main article
  > .newspaper,
  > .tweet,
  > .link,
  > .video,
  > .comment
    grid-column: 1 / span 2
    grid-row: 1
    margin: 0
    max-width: none

    @media (max-width: $mobile)
      grid-column: 1 / span 1
      grid-row: 1

    timeline-post--article--content
      column-count: 2

    .timeline-post--video--content
      grid-template-columns: 1fr

  .video + .editorial-post--editorial

    .tweet-attachment-link-view
      display: none

  .editorial-post-tweet-editor
    article
      margin: 0

    .timeline-post--tweet
        margin: 0

  //- tweets
  .editorial-post--editorial
    align-self: center
    grid-column: 3 / span 1
    grid-row: 1

    article
      margin: 0
      background: #F2ECEC

      .timeline-post--tweet
        margin: 0

      .tweet-attachment-link-view
        display: none //- TODO: refactor so it's not done over CSS

      .tweet-attachment-gallery

        img
          display: block
          height: auto
          max-height: 288px

        &.gallery-1,
        &.gallery-2,
        &.gallery-3,
        &.gallery-4
          grid-template-rows: minmax(auto, max-content)

        &.gallery-2
          grid-template-columns: 100%

        &.gallery-1 img
          object-fit: contain

      .tweet-attachment-video-view video
        max-height: 288px

    @media (max-width: $mobile)
      grid-column: 2 / span 1
      grid-row: 1

  &.is-before
    .newspaper
      grid-column: 2 / span 2

      @media (max-width: $mobile)
        grid-column: 2 / span 1
        grid-row: 1

    .video
      grid-column: 2 / span 2
      grid-row: 1

    .editorial-post--editorial
      grid-column: 1 / span 1


//- Normal Post
.normal-post
  position: relative

  .post
    border: 1px solid #eee
    box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff
</style>

