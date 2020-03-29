<template>
  <PostBase :post="post">
    <div class="post-body">
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <nuxt-link v-else :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link>
      </h2>

      <div class="post-body--content">
        <div v-html="perex"></div>
        <div class="timeline-post--continue-reading" v-if="post.timeRead && !post.draft">
          <template v-if="post.content.protected">
            <a :href="post.source" target="_blank">{{ $t('Read the article') }}</a>
            ({{ post.timeRead }} {{ $t('read') }})
          </template>
          <template v-else>
            <div>
              <nuxt-link :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }, hash: '#continue'}">
                {{ $t('Continue reading') }}
              </nuxt-link>
            </div>
            <!--div v-else>
              {{ $t('Subscribe newspaper to continue reading') }}
            </div-->
            ({{ post.timeRead }} {{ $t('read') }})
          </template>
        </div>
      </div>
    </div>

    <template #page-controls><slot name="page-controls"></slot></template>
    <template #global-controls><slot name="global-controls"></slot></template>
  </PostBase>
</template>

<script>
import PostBase from './PostBase';

export default {
  name: 'PostArticle',

  props: {
    post: Object,
  },

  components: {
    PostBase
  },

  computed: {
    perex() {
      const { baseURL } = this.$axios.defaults
      const { perex } = this.post.content
      let URL

      if (process.server) {
        URL = require('universal-url').URL
      } else {
        URL = window.URL
      }

      const replaceUrl = (src, callback) => {
        // universal URL can't parse url without protocol
        const url = new URL(src.startsWith('//') ? `http:${src}` : src)
          if (url.hostname !== 'kairly.com') {
            callback(`${baseURL}/p?post=${encodeURIComponent(this.post.slug)}&size=timeline&src=${encodeURIComponent(src)}`)
          }
      }

      // don't use template element! querySelectorAll ignores templates
      if (process.server) {
        // document (and createElement is not defined on server)
        const cheerio = require('cheerio')
        const $ = cheerio.load(perex)
        $('img').each(function(i, img) {
          replaceUrl($(img).attr('src'), src => {
            $(img).attr('src', src)
          })
        })
        return $.html()
      } else {
        const fragment = document.createElement('div')
        fragment.innerHTML = perex
        fragment.querySelectorAll('img').forEach(img => {
          replaceUrl(img.src, src => { img.src = src })
        })
        //post.content.perex
        return fragment.innerHTML
      }
    }
  },

  mounted() {

  }
}
</script>


<style lang="sass">
@import './styles/components/article-perex'
@import './styles/mixins/perex-button'

.newspaper > .post-body
  font-family: $ff-serif

  //- Title
  > h2
    display: block
    margin-bottom: $baseline / 4

    font-size: $fs-1
    font-weight: 600
    line-height: 1.58

    @media (max-width: $mobile)
      font-size: $fs-0

    a
      color: #000

  a
    color: $c-base

//- Content
.post-body--content
  position: relative

  column-rule: 1px dotted #ddd
  column-gap: $baseline

  line-height: 1.58
  hyphens: auto

  +article-perex

.newspaper .post-body--content
  column-count: 3
  
  @media (max-width: $mobile)
    column-count: 2
    column-gap: $baseline / 2

    font-size: 15px
    line-height: 1.58

  //- Continue Reading
  .timeline-post--continue-reading
    +perex-button
    
</style>
