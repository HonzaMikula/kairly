<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="100"
  >
    <Welcome v-if="!loading && issues.length === 0"/>

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

      <div v-if="loading">Loading...</div>
    </div>
  </timeline-view>
</template>

<script>
import * as api from '@/api'
import { mapState } from 'vuex'

import Welcome from '@/components/Welcome'
import postArticle from '@/components/posts/article'
import postBlog from '@/components/posts/blog'
import postNewspaper from '@/components/posts/newspaper'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'Timeline',

  data: function () {
    return {
      'loading': true,
      'page': 1,
      'lastPage': null,
      'issues': []
    }
  },

  components: {
    postArticle,
    postBlog,
    postNewspaper,
    postTweet,
    postPicture,
    Welcome,
  },

  computed: {
    ...mapState({
      editions: state => state.editions || []
    })
  },

  methods: {
    handleTimelineData: function(timeline) {
      timeline.issues.forEach(issue => this.issues.push(issue))
      this.lastPage = timeline.lastPage
      this.loading = false
    },

    loadMore: function() {
      if (this.page < this.lastPage) {
        this.page += 1
        this.loading = true
        api.getTimeline(this.page).then(this.handleTimelineData)
      }
    }
  },

  created: function () {
    if (this.editions === []) {
      this.issues = []
      this.lastPage = 1
      this.loading = false
    } else {
      api.getTimeline().then(this.handleTimelineData)
    }
  }
}
</script>
