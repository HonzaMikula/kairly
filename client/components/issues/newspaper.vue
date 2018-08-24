<template>
  <timeline-newspaper>
    <header>
      <h1>
        <nuxt-link :to="{name: 'author-newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">{{ issue.newspaper.title }}</nuxt-link>&nbsp;<nuxt-link :to="{name: 'author-newspaper-issue', params: {author: newspaper.editor.id, newspaper: newspaper.name, issue: issue.number}}">#{{ issue.number }}</nuxt-link>
      </h1>

      <p>
        <timeline-newspaper--editor>
          <nuxt-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
            <img v-if="issue.newspaper.editor.picture" :src="newspaper.editor.picture" :alt="newspaper.editor.name" />
            {{ newspaper.editor.name }}
          </nuxt-link>
        </timeline-newspaper--editor>
        •
        {{ newspaper.periodicity.frequency }}
        •
        {{ issue.time | moment('calendar')}}
      </p>
    </header>
    <slot></slot>
  </timeline-newspaper>
</template>

<script>
export default {
  name: 'issue-newspaper',
  props: ['issue'],

  computed: {
    newspaper() {
      return this.issue.newspaper
    }
  }
}
</script>
