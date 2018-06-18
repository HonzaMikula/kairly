<template>
  <timeline-edition>
    <header>
      <h1>
        <router-link :to="`/editions/${issue.edition.id}`">{{ issue.edition.title }}</router-link>&nbsp;<router-link :to="`/editions/${issue.edition.id}/${issue.number}`">#{{ issue.number }}</router-link>
      </h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="{name: 'author', params: {authorId: issue.author.id}}">
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </router-link>
        </timeline-edition--editor>
        •
        {{ issue.edition.periodicity.frequency }}
        •
        {{ issue.time | moment('calendar')}}
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
