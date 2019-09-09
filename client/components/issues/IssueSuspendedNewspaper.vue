<template>
  <timeline-newspaper class="issue-unreleased">
    <header>
      <h1>
        <nuxt-link :to="`/${newspaper.editor.id}/${newspaper.name}`">
          <slot name="newspaper-title">{{ issue.newspaper.title }}</slot>
        </nuxt-link>
      </h1>

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

    <article>
      {{ $t('Your susbscription were suspended.') }}
    </article>

  </timeline-newspaper>
</template>

<script>
export default {
  name: 'IssueSuspendedNewspaper',
  props: ['issue', 'hideDate'],

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

<style lang="sass">
</style>
