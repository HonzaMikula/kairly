<template>
  <div class="recommendations-post-view">
    <template v-if="recommendedIssues.length > 0">
      <h2>{{ $t('Recommended issues') }}</h2>

      <div v-for="item in recommendedIssues" :key="item.id">
        <h3>
          <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: item.ref.newspaper.editor.id, newspaper: item.ref.newspaper.name, issue: item.ref.number}}">
            {{ item.ref.newspaper.title }} ({{ item.ref.newspaper.time | moment('D. M. YYYY') }})
          </nuxt-link>
        </h3>

        <p>
          {{ item.ref.posts.map(post => post.content.title || post.author.name).filter(title => title).join(' • ') }}
        </p>

        <footer class="recommendations-post--author">
          <nuxt-link :to="{name: 'author', params: {author: item.ref.newspaper.editor.id}}">
            <AuthorPicture :author="item.ref.newspaper.editor" />
            {{ item.ref.newspaper.editor.name }}
          </nuxt-link>
        </footer>
      </div>
    </template>

    <template v-if="recommendedPosts.length > 0">
      <h2>{{ $t('Recommended posts') }}</h2>

      <div v-for="item in recommendedPosts" :key="item.id">
        <h3>
          <nuxt-link :to="{ name: 'author-post', params: { author: item.ref.author.id, post: item.ref.slug }}">
            {{ item.ref.content.title }}
          </nuxt-link>
        </h3>

        <footer class="recommendations-post--author">
          <nuxt-link :to="{name: 'author', params: {author: item.ref.author.id}}">
            <AuthorPicture :author="item.ref.author" />
            {{ item.ref.author.name }}
          </nuxt-link>
        </footer>
      </div>
    </template>
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'

export default {
  name: 'PostRecommendations',

  components: {
    AuthorPicture
  },

  props: {
    post: Object,
  },

  computed: {
    recommendedPosts () {
      return this.post.posts
    },

    recommendedIssues () {
      return this.post.issues
    }
  }
}
</script>

<style lang="sass">
//- Recommendations Post -//
.recommendations-post-view
  display: block
  border-radius: 6px
  margin-bottom: $baseline / 2
  padding: $baseline / 2
  max-width: 576px

  background: #fff

  //- headings
  h2
    margin-bottom: $baseline / 2
    font-size: $fs-1
    font-weight: 600

    &::before
      +fa-icon()
      @extend .fas

      position: relative
      top: -2px

      margin-right: $baseline / 4

      color: #777

      content: fa-content($fa-var-star)

  div
    margin-bottom: $baseline

    font-family: $ff-serif

    &:last-of-type
      margin-bottom: 0

  //- title
  h3
    margin-bottom: $baseline / 4

    font-weight: 600

  a
    color: #000

  //- perex
  p
    margin-bottom: $baseline / 4

//- author
.recommendations-post--author a
  display: inline-flex

  font-family: $ff-sans

  img
    border-radius: 100%
    height: $baseline
    margin-right: $baseline / 4
    width: $baseline

</style>
