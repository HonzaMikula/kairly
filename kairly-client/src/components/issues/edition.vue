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

    <PostWrapper
      v-for="post in issue.posts"
      :post="post"
      :isSubscribed="isSubscribed"
      :key="post.id"
    />
  </div>
</template>

<script>
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'issue-edition',
  props: ['issue', 'isSubscribed'],

  components: {
    PostWrapper
  }
}
</script>
