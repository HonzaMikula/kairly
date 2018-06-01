<template>
  <timeline-edition>
    <header>
      <h1>
        {{issue.title}}
        <router-link :to="`/editions/${issue.edition.id}/${issue.id}`">
          <span style="font-size: 18px">&#x1f517;</span>
        </router-link>
      </h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="issue.author.url">
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </router-link>
        </timeline-edition--editor>
        •
        {{issue.edition.period}}
        •
        {{issue.time | moment('calendar')}}
      </p>
    </header>
    <slot></slot>
  </timeline-edition>
</template>

<script>
export default {
  name: 'issue-edition',
  props: ['issue']
}
</script>
