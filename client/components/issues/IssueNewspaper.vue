<template>
  <timeline-newspaper>
    <header>
      <h1 :id="`issue-newspaper-${_uid}`">
        <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: newspaper.editor.id, newspaper: newspaper.name, issue: issue.number}}">
          <slot name="newspaper-title">{{ issue.newspaper.title }}</slot>
        </nuxt-link>
      </h1>

      <NewspaperPopup
        :target="`issue-newspaper-${_uid}`"
        :newspaper="newspaper"
      />

      <p>
        <timeline-newspaper--editor>
          <nuxt-link
            :to="{name: 'author', params: {author: newspaper.editor.id}}"
            :id="`issue-newspaper-author-${_uid}`">
            <img
              v-if="issue.newspaper.editor.picture"
              :src="newspaper.editor.picture"
              :alt="newspaper.editor.name"
            />
            {{ newspaper.editor.name }}
          </nuxt-link>
        </timeline-newspaper--editor>
        <span>• {{ frequencyLabel }}</span>
        <template v-if="!hideDate"> • {{ issue.time | moment('calendar')}}</template>
      </p>

      <AuthorPopup
        :target="`issue-newspaper-author-${_uid}`"
        :author="newspaper.editor"
      />

    </header>
    <slot/>
  </timeline-newspaper>
</template>

<script>

import AuthorPopup from '@/components/widgets/AuthorPopup'
import NewspaperPopup from '@/components/widgets/NewspaperPopup'

export default {
  name: 'IssueNewspaper',
  props: ['issue', 'hideDate'],

  components: {
    AuthorPopup,
    NewspaperPopup,
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
