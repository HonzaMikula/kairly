<template>
  <timeline-edition>
    <header>
      <h1>
        <router-link :to="`/editions/${issue.edition.id}`">{{ issue.edition.title }}</router-link>&nbsp;<router-link :to="`/editions/${issue.edition.id}/${issue.number}`">#{{ issue.number }}</router-link>
      </h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="{name: 'author', params: {authorId: issue.edition.editor.id}}">
            <img v-if="issue.edition.editor.picture" :src="issue.edition.editor.picture" :alt="issue.edition.editor.name" />
            {{ issue.edition.editor.name }}
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
