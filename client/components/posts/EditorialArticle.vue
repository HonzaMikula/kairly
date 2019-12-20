<template>
  <div class="editorial-post--editorial article">
    <article role="article" class="post newspaper editorial">
      <header>
        <picture>
          <nuxt-link :to="{name: 'author', params: {author: editorial.author.id}}">
            <AuthorPicture :author="editorial.author" />
          </nuxt-link>
        </picture>

        <h3>
          <nuxt-link :to="{name: 'author', params: {author: editorial.author.id}}">
            {{ editorial.author.name }}<span v-if="editorial.author.medium">, {{editorial.author.medium}}</span>
          </nuxt-link>
        </h3>
      </header>
      <timeline-post--article>
        <h2>{{ editorial.title }}</h2>
        <timeline-post--article--content v-html="editorial.content" />
      </timeline-post--article>
    </article>
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'

export default {
  name: 'EditorialArticle',

  props: {
    editorial: Object
  },

  components: {
    AuthorPicture
  },
}
</script>
<style lang="sass">
.editorial-post .editorial-post--editorial.article
  align-self: start

.editorial-post--editorial .post.newspaper.editorial
  timeline-post--article--content
    column-count: 1

</style>
