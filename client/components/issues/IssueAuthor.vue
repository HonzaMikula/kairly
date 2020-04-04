<template>
  <div class="timeline-newspaper">
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

    <slot />

    <PostIssue
      v-for="item in issue.issues"
      :key="item.id"
      :post="item"
    />
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorPopup from '@/components/widgets/AuthorPopup'
import PostIssue from '@/components/posts/PostIssue'

export default {
  name: 'IssueAuthor',

  components: {
    AuthorPicture,
    AuthorPopup,
    PostIssue,
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
