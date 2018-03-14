<template>
  <div>
    <timeline-edition>
      <h1>{{issue.title}}</h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="issue.author.url">
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </router-link>
        </timeline-edition--editor>
        •
        {{issue.period}}
        •
        {{issue.time | moment('calendar')}}
      </p>
    </timeline-edition>

    <component
      v-for="post in issue.posts"
      :is="'post-' + post.type"
      :post="post"
      :isSubscribed="isSubscribed"
      :key="post.id"
      v-on:readlater="readLaterMessage()">
    </component>
  </div>
</template>

<script>
import postNewspaper from '@/components/posts/newspaper'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'Issue',
  props: ['issue', 'isSubscribed'],

  components: {
    postNewspaper,
    postTweet,
    postPicture,
  },

  methods: {
    readLaterMessage() {
      console.log('TODO')
    }
  }
}
</script>
