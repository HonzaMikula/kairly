<template>
  <main>
    <explore--top-editions>
      <h2>Recent Issues</h2>

      <div>
        <EditionWidget
          v-for="issue in issues"
          :key="`${issue.edition.fullName}#${issue.number}`"
          :edition="issue.edition"
        />
      </div>

    </explore--top-editions>

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

import EditionWidget from '@/components/widgets/EditionWidget'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'ExploreContent',

  components: {
    EditionWidget,
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
