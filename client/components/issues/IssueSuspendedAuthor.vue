<template>
  <div class="timeline-newspaper issue-unreleased">
    <header>
      <h1>
        <nuxt-link
          :id="`issue-author-${$_uid}`"
          :to="{name: 'author', params: {author: issue.author.id}}"
        >
          <AuthorPicture :author="issue.author" />
          {{ issue.author.name }}
        </nuxt-link>
      </h1>

      <AuthorPopup
        :target="`issue-author-${$_uid}`"
        :author="issue.author"
      />

      <p>
        {{ localizedTitle() }}
        •
        {{ issue.time | moment('calendar') }}
      </p>
    </header>

    <article>
      {{ $t('Your susbscription were suspended.') }}
    </article>
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorPopup from '@/components/widgets/AuthorPopup'

export default {
  name: 'IssueSuspendedAuthor',

  components: {
    AuthorPicture,
    AuthorPopup,
  },
  props: {
    issue: { type: Object, required: true }
  },

  methods: {
    localizedTitle () {
      // each constant must be wrapped to $t
      const { title } = this.issue
      if (title === '6× per day') { return this.$t('6× per day') }
      if (title === '3× per day') { return this.$t('3× per day') }
      if (title === 'Daily summary') { return this.$t('Daily summary') }
      if (title === 'Weekly summary') { return this.$t('Weekly summary') }
      return title // should never happen
    }
  }

}
</script>

<style lang="sass">
/* shares issue-unreleased style from unreleased-newspaper.vue */
</style>
