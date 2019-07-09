<template>
  <section class="editorial-post" :class="{'is-before': isBefore}">
    <PostArticle :post="post" :isSubscribed="isSubscribed">
      <template slot="controls"><slot name="controls"></slot></template>
      <template slot="extendedControls"><slot name="extendedControls"></slot></template>
    </PostArticle>

    <component 
      :is="'editorial-'+ editorialComponent"
      @saveEditorialArticle="setType('article')"
    />
  </section>
</template>

<script>
// TODO
// - component is for distinguishing selecting tweets
// - controls for Manage newspaper
// - turn on this mode

import PostArticle from './PostArticle'
import EditorialTweet from './EditorialTweet'
import EditorialArticle from './EditorialArticle'
import EditorialEditor from './EditorialEditor'

export default {
  name: 'Editorial',

  props: ['post', 'isSubscribed', 'editorial'],

  components: {
    PostArticle,
    EditorialTweet,
    EditorialArticle,
    EditorialEditor
  },

  data() {
    return {
      isBefore: false, //- editorials should appear on left on right
      editorialComponent: 'editor' //- to quickly change component: article, tweets
    }
  },

  methods: {
    setType(type) {
      this.editorialComponent = type
    }
  },

  created() {
    console.log(this.editorial)
    if (this.editorial == 'article')
      this.editorialComponent = 'editor'
    else
      this.editorialComponent = this.editorial
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
