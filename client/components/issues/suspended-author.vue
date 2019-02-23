<template>
  <timeline-newspaper class="issue-unreleased">
    <header>
      <h1>
        <nuxt-link :to="{name: 'author', params: {author: issue.author.id}}">
          <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
          {{ issue.author.name }}
        </nuxt-link>
      </h1>

      <p>
        {{ localizedTitle() }}
        •
        {{ issue.time | moment('calendar') }}
      </p>
    </header>


    <article>
      {{ $t('Your susbscription were suspended.') }}
    </article>

  </timeline-newspaper>
</template>

<script>
export default {
  name: 'issue-suspended-author',
  props: ['issue'],

  methods: {
    localizedTitle() {
      // each constant must be wrapped to $t
      const { title } = this.issue
      if (title === '6× per day') return this.$t('6× per day')
      if (title === '3× per day') return this.$t('3× per day')
      if (title === 'Daily summary') return this.$t('Daily summary')
      if (title === 'Weekly summary') return this.$t('Weekly summary')
      return title // should never happen
    }
  }

}
</script>

<style lang="sass">
/* shares issue-unreleased style from unreleased-newspaper.vue */
</style>
