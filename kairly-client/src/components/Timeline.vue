<template>
  <timeline-view>
    <div v-for="edition in editions" :key="edition.id">
      <timeline-edition>
        <h1>{{edition.title}}</h1>

        <p>
          <timeline-edition--editor>
            <img v-if="edition.author.picture" :src="edition.author.picture" :alt="edition.author.name" />
            {{edition.author.name}}
          </timeline-edition--editor>
          •
          {{ edition.edition }}
          •
          {{edition.time | moment('calendar')}}
        </p>
      </timeline-edition>

      <component
        v-for="post in edition.posts"
        :is="post.testType"
        :post="post"
        :key="post.id"
        v-on:readlater="readLaterMessage()">
      </component>

    </div>
  </timeline-view>
</template>

<script>
import * as api from '@/api'

import postArticle from '@/components/posts/article'
import postBlog from '@/components/posts/blog'
import postNewspaper from '@/components/posts/newspaper'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'Timeline',

  data: function () {
    return {
      'editions': []
    }
  },

  components: {
    postArticle,
    postBlog,
    postNewspaper,
    postTweet,
    postPicture
  },

  created: function () {
    api.getTimeline().then(timeline => {
      this.editions = timeline.editions
    })
  }
}
</script>
