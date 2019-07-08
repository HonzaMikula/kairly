<template>
  <section class="editorial-post" :class="{'is-before': isBefore}">
    <PostArticle :post="post" :isSubscribed="isSubscribed" />

    <component :is="'editorial-'+ editorialComponent" />
  </section>
</template>



<script>
// Docs
// - component is for distinguishing tweets, article, writing article, selecting tweets
//
import PostArticle from './PostArticle'
import EditorialTweets from './EditorialTweets'
import EditorialArticle from './EditorialArticle'
import EditorialEditor from './EditorialEditor'

export default {
  name: 'Editorial',

  props: ["post", "isSubscribed"],

  components: {
    PostArticle,
    EditorialTweets,
    EditorialArticle,
    EditorialEditor
  },

  data() {
    return {
      isBefore: false, //- editorials should appear on left on right
      editorialComponent: 'editor' //- to quickly change component: article, tweets
    }
  }
}
</script>
<style lang="sass">
.editorial-post
  display: grid
  grid-template-columns: 1fr 1fr 1fr
  border: 1px solid #eee
  margin-bottom: $baseline / 2

  background: #f5f5f5

  //- main article
  .newspaper
    grid-column: 1 / span 2
    grid-row: 1
    margin: 0

    timeline-post--article--content
      column-count: 2

  //- tweets
  .editorial-post--editorial
    align-self: center
    grid-column: 3 / span 1
    grid-row: 1

    article
      background: #f5f5f5

  &.is-before
    .newspaper
      grid-column: 2 / span 2

    .editorial-post--editorial
      grid-column: 1 / span 1
</style>
