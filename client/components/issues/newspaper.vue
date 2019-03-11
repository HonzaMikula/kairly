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
    <footer>
      <recommend-button-issue :issue="issue" />
    </footer>
  </timeline-newspaper>
</template>

<script>
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'

export default {
  name: 'issue-newspaper',
  props: ['issue', 'hideDate'],

  components: {
    RecommendButtonIssue
  },

  computed: {
    newspaper() {
      return this.issue.newspaper
    },

    frequencyLabel() {
      const { frequency } = this.newspaper.periodicity
      if (frequency == '6x_per_day') return this.$t('6× per day')
      if (frequency == '3x_per_day') return this.$t('3× per day')
      if (frequency == 'weekly') return this.$t('Weekly')
      if (frequency == 'daily') return this.$t('Daily')
      return ''
    }
  }

}
</script>
