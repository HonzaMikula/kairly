<template>
  <div>
    <timeline-edition>
      <h1>
        <router-link :to="issue.author.url">
          <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
          {{issue.author.name}}
        </router-link>
      </h1>

      <p>
        Daily summary
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

    <post-issue>
      <timeline-post--header>
        <a href="">
          <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg"/>
        </a>

        <timeline-post--header--author>
          <a href="">Jan Mikula</a>
        </timeline-post--header--author>

        <timeline-post--header--info>
          Last Friday at 10:41 PM
        </timeline-post--header--info>

      </timeline-post--header>

      <div>
        <h2><a href="/editions/janmikula/malostranskenoviny">Malostranské noviny #14</a></h2>
        <picture>
          <a href="/editions/janmikula/malostranskenoviny">
            <img src="http://kairly.com/media/editions/malostranskenoviny.jpg"/>
          </a>
        </picture>
        <p>Přehled toho nejzajímavějšího, co se událo v české politice.</p>
      </div>
    </post-issue>

  </div>
</template>

<script>
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'issue-author',
  props: ['issue', 'isSubscribed'],

  components: {
    PostWrapper
  }
}
</script>
