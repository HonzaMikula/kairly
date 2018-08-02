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

  </main>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import IssueWidget from '@/components/widgets/IssueWidget'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'ExploreContent',

  components: {
    IssueWidget,
    PostWrapper
  },

  props: {
    tab: Object
  },

  data() {
    return {
      issues: [],
      posts: [],
    }
  },

  created() {
    api.getRecentIssues().then(issues => this.issues = issues)
    api.getRecentPosts().then(posts => this.posts = posts)
  }
}
</script>

<style lang="sass">
</style>
