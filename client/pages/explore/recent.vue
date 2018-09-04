<template>
  <main>
    <explore--top-newspapers>
      <h2>Recent Issues</h2>

      <div>
        <IssueWidget
          v-for="issue in issues"
          :key="`${issue.newspaper.fullName}#${issue.number}`"
          :issue="issue"
        />
      </div>

    </explore--top-newspapers>

    <section class="explore-recent">
      <h2>Recent Posts</h2>

      <PostWrapper
        v-for="post in posts"
        :post="post"
        :isSubscribed="true"
        :key="post.id"
      />
    </section>

    <portal to="explore-header">Most Recent</portal>

  </main>
</template>

<script>
import IssueWidget from '@/components/widgets/IssueWidget'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'ExploreRecentTab',

  //auth: false,

  components: {
    IssueWidget,
    PostWrapper
  },

  head() {
    return {
      title: 'Explore - Most Recent',
    }
  },

  async asyncData({ app }) {
    const [issues, posts] = await Promise.all([
      app.$axios.$get('/recent/issues'),
      app.$axios.$get('/recent/posts')
    ])
    return { issues, posts }
  }
}
</script>

<style lang="sass">
</style>
