<template>
  <timeline-edition>
    <header>
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
    </header>
    

    <slot></slot>

    <post-issue v-for="item in issue.issues" :key="item.id">
      <div >
        <h2><a :href="'/editions/' + item.edition.id">{{ item.title }}</a></h2>
        <picture>
          <a :href="'/editions/' + item.edition.id">
            <img :src="item.edition.picture"/>
          </a>
        </picture>
        <p>{{ item.edition.description }}</p>
      </div>
    </post-issue>
  </timeline-edition>
</template>

<script>
export default {
  name: 'issue-author',
  props: ['issue']
}
</script>
