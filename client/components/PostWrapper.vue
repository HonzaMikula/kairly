<template>
  <section 
    :class="{'editorial-post': !!editorial, 'is-before': editorial && editorial.position === 'left'}"
    v-on:scroll.passive="onScroll">
    <component
      :is="'post-' + postType"
      :key="post.id"
      :post="post"
      :isSubscribed="isSubscribed"
    >
      <template slot="author">
        <slot name="author"></slot>
      </template>

      <template slot="extendedControls">
        <slot name="extendedControls"></slot>
      </template>

      <template slot="controls">
        <slot name="controls"></slot>
      </template>
    </component>

    <slot name="editorial">
      <!-- :is="'editorial-' + post.editorial.type" -->
      <component
        v-if="editorial"
        :is="'editorial-' + editorial.type"
        :editorial="editorial"
      />
    </slot>
  </section>
</template>

<script>
import PostArticle from '@/components/posts/PostArticle'
import PostLink from '@/components/posts/PostLink'
import PostTweet from '@/components/posts/PostTweet'
import PostPicture from '@/components/posts/PostPicture'
import PostRecommendations from '@/components/posts/PostRecommendations'

import EditorialTweets from '@/components/posts/EditorialTweets'
import EditorialArticle from '@/components/posts/EditorialArticle'

export default {
  name: 'PostWrapper',
  props: {
    post: Object,
    isSubscribed: Boolean,
    editorial: Object,  // right or left
  },

  components: {
    PostArticle,
    PostLink,
    PostTweet,
    PostPicture,
    PostRecommendations,
    EditorialTweets,
    EditorialArticle
  },

  computed: {
    //- TEMP hack - we can get rid of it after migration
    postType() {
      // if (this.editorial == 'article' || this.editorial == 'tweet') {
      //   return 'editorial'
      // }
      if (this.post.type == 'newspaper') {
        return 'article' // TODO: back to 'article'
      }
      else {
        return this.post.type
      }
    }
  }
}
</script>

<style lang="sass">
.editorial-post
  display: grid
  grid-template-columns: 1fr 1fr 1fr
  margin-bottom: $baseline / 2

  background: #F2ECEC

  @media (max-width: $mobile)
    grid-template-columns: calc(100vw - (#{$baseline} * 1.5)) 60vw

    overflow: auto
    scroll-behavior: smooth
    -webkit-overflow-scrolling: touch

    &.is-before
      grid-template-columns: 60vw calc(100vw - (#{$baseline} * 1.5))

  //- main article
  .newspaper,
  .link
    grid-column: 1 / span 2
    grid-row: 1
    margin: 0

    @media (max-width: $mobile)
      grid-column: 1 / span 1
      grid-row: 1
      
    timeline-post--article--content
      column-count: 2

  .editorial-post-tweet-editor
    article
      margin: 0

    timeline-post--tweet
        margin: 0

  //- tweets
  .editorial-post--editorial
    align-self: center
    grid-column: 3 / span 1
    grid-row: 1

    article
      margin: 0
      background: #F2ECEC

      timeline-post--tweet
        margin: 0

        .tweet-attachment-link-view
          display: none //- TODO: refactor so it's not done over CSS

    @media (max-width: $mobile)
      grid-column: 2 / span 1
      grid-row: 1

  &.is-before
    .newspaper
      grid-column: 2 / span 2

      @media (max-width: $mobile)
        grid-column: 2 / span 1
        grid-row: 1

    .editorial-post--editorial
      grid-column: 1 / span 1

</style>

