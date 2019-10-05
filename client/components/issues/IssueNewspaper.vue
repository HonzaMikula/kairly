<template>
  <timeline-newspaper>
    <header>
      <h1 :id="`issue-newpaper-${randomId}`">
        <nuxt-link :to="{name: 'author-newspaper-issue', params: {author: newspaper.editor.id, newspaper: newspaper.name, issue: issue.number}}">
          <slot name="newspaper-title">{{ issue.newspaper.title }}</slot>
        </nuxt-link>
      </h1>

      <b-popover
        :target="`issue-newpaper-${randomId}`"
        placement="bottom"
        :delay="{ show: 400, hide: 100 }"
        triggers="hover"
        @click.stop
      >
        <AuthorWidget :author="newspaper.editor" />
      </b-popover>

      <p>
        <timeline-newspaper--editor>
          <nuxt-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
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
    </header>
    <slot/>
  </timeline-newspaper>
</template>

<script>
import { BPopover } from 'bootstrap-vue'
import AuthorPopup from '@/components/widgets/AuthorPopup'

export default {
  name: 'IssueNewspaper',
  props: ['issue', 'hideDate'],

  components: {
    BPopover,
    AuthorPopup
  },

  computed: {
    newspaper() {
      return this.issue.newspaper
    },

    randomId() {
      return Math.floor(Math.random() * 10000000)
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
