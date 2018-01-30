<template>
  <timeline-view v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loading"
    infinite-scroll-distance="100"
  >
    <timeline-welcome>
      <h1>Welcome to Kairly</h1>
      <p>Start with selecting editions you want to subscribe.</p>

      <timeline-welcome--my-editions>
        <my-editions--item v-for="edition in [1,2,3]" :key="edition.id">
          <picture>
            <img src="http://kairly.com/media/editions/volby_omSw6dr.jpg" alt="" />
          </picture>

          <h2>Prezidentské volby</h2>

          <p>Nejdůležitější informace z probíhajících prezidentských voleb.</p>

          <my-editions--item--author>
            <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt=""/>
            Jan Mikula
          </my-editions--item--author>

          <my-editions--item--subscribe>
            <button>Subscribe</button>
            <p>
              10 CZK per month
              •
              {{ 123 }} subscribers
              •
              #{{ 12 }}
            </p>
          </my-editions--item--subscribe>

        </my-editions--item> 
      </timeline-welcome--my-editions>

      <timeline-welcome--more-editions>
        <router-link to='/my-editions'>View more editions</router-link>
      </timeline-welcome--more-editions>
    </timeline-welcome>

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
    postPicture
  },

  methods: {
    handleTimelineData: function(timeline) {
      timeline.issues.forEach(issue => this.issues.push(issue))
      this.lastPage = timeline.last_page
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
    api.getTimeline().then(this.handleTimelineData)
  }
}
</script>
