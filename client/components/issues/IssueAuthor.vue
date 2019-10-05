<template>
  <timeline-newspaper>
    <header>
      <h1 :id="`issue-author-${$_uid}`">
        <nuxt-link :to="{name: 'author', params: {author: issue.author.id}}">
          <img
            v-if="issue.author.picture"
            :src="issue.author.picture"
            :alt="issue.author.name"
          />
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

    <slot />

    <PostIssue
      v-for="item in issue.issues"
      :post="item"
      :key="item.id"
    />
  </timeline-newspaper>
</template>

<script>
import PostIssue from '@/components/posts/PostIssue'
import AuthorPopup from '@/components/widgets/AuthorPopup'

export default {
  name: 'IssueAuthor',
  props: {
    issue: Object
  },

  components: {
    AuthorPopup,
    PostIssue,
  },

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
