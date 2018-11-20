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
        <span>• {{ frequencyLabel }}</span>
        <template v-if="!hideDate"> • {{ issue.time | moment('calendar')}}</template>
      </p>
    </header>
    <slot></slot>
  </timeline-newspaper>
</template>

<script>
export default {
  name: 'issue-newspaper',
  props: ['issue', 'hideDate'],

  computed: {
    newspaper() {
      return this.issue.newspaper
    },

    frequencyLabel() {
      const { frequency } = this.newspaper.periodicity
      if (frequency == '6x_per_day') return '6× per day'
      if (frequency == '3x_per_day') return '3× per day'
      if (frequency == 'weekly') return 'Weekly'
      if (frequency == 'daily') return 'Daily'
      return ''
    }
  }

}
</script>
