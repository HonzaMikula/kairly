<template>
  <timeline-newspaper>
    <header>
      <h1>
        <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: newspaper.editor.id, newspaper: newspaper.name, issue: issue.number}}">
          <slot name="newspaperTitle">{{ issue.newspaper.title }}</slot>
        </nuxt-link>
      </h1>

      <p>
        <timeline-newspaper--editor>
          <nuxt-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
            <img v-if="issue.newspaper.editor.picture" :src="newspaper.editor.picture" :alt="newspaper.editor.name" />
            {{ newspaper.editor.name }}
          </nuxt-link>
        </timeline-newspaper--editor>
        <template v-if="!hideNumber">• #{{ issue.number }}</template>
        • {{ newspaper.periodicity.frequency }}
        <template v-if="!hideDate"> • {{ issue.time | moment('calendar')}}</template>
      </p>
    </header>
    <slot></slot>
  </timeline-newspaper>
</template>

<script>
export default {
  name: 'issue-newspaper',
  props: ['issue', 'hideDate', 'hideNumber'],

  computed: {
    newspaper() {
      return this.issue.newspaper
    }
  }
}
</script>
