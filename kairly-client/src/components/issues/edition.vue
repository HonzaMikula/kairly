<template>
  <timeline-edition>
    <header>
      <h1>
        <router-link :to="{name: 'edition', params: {author: edition.editor.id, edition: edition.name}}">{{ issue.edition.title }}</router-link>&nbsp;<router-link :to="{name: 'issue', params: {author: edition.editor.id, edition: edition.name, issue: issue.number}}">#{{ issue.number }}</router-link>
      </h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="{name: 'author', params: {author: edition.editor.id}}">
            <img v-if="issue.edition.editor.picture" :src="edition.editor.picture" :alt="edition.editor.name" />
            {{ edition.editor.name }}
          </router-link>
        </timeline-edition--editor>
        •
        {{ edition.periodicity.frequency }}
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
  props: ['issue'],

  computed: {
    edition() {
      return this.issue.edition
    }
  }
}
</script>
