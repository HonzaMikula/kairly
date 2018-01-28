<template>
  <timeline-view>
    <div v-for="issue in issues" :key="issue.id">
      <timeline-edition>
        <h1>{{issue.title}}</h1>

        <p>
          <timeline-edition--editor>
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </timeline-edition--editor>
          •
          {{issue.period}}
          •
          {{issue.time | moment('calendar')}}
        </p>
      </timeline-edition>

      <component
        v-for="post in issue.posts"
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
      'issues': []
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
      this.issues = timeline.issues
    })
  }
}
</script>
