<template>
  <timeline-newspaper>
    <header>
      <h1>
        <router-link :to="{name: 'author', params: {author: issue.author.id}}">
          <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
          {{ issue.author.name }}
        </router-link>
      </h1>

      <p>
        {{ issue.title }}
        •
        {{ issue.time | moment('calendar') }}
      </p>
    </header>


    <slot></slot>

    <PostIssue
      v-for="item in issue.issues"
      :post="item"
      :key="item.id"
     />

    <!--
    <post-issue v-for="item in issue.issues" :key="item.id">

    </post-issue>-->
  </timeline-newspaper>
</template>

<script>
import PostIssue from '@/components/posts/issue'

export default {
  name: 'issue-author',
  props: ['issue'],

  components: {
    PostIssue
  },
}
</script>
