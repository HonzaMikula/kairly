<template>
  <AppLayout :name="$t('Edit a post')">
    <div class="edit-post">
      <EditArticle v-if="post.type == 'newspaper'" :post="post" :buttonTitle="$t('Save')" @submit="savePost" />
      <EditTweet v-if="post.type == 'tweet'" :post="post" :buttonTitle="$t('Save')" @submit="savePost" />
    </div>
  </AppLayout>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import EditArticle from '@/components/editor/EditArticle'
import EditTweet from '@/components/editor/EditTweet'

export default {
  name: 'Posts',

  head() {
    return {
      title: this.$t('My Posts – Kairly')
    }
  },

  components: {
    AppLayout,
    EditArticle,
    EditTweet,
  },

  methods: {
    async savePost(data) {
      const { post } = await this.$axios.$patch(`/drafts/${this.post.id}`, data)
      if (post.draft) {
        this.$router.push("/posts")
      } else {
        this.$router.push("/posts/published")
      }
    }
  },

  async asyncData({ app, store, params }) {
    const { post } = await app.$axios.$get(`/drafts/${params.postId}`)
    return {
      post
    }
  }
}
</script>

<style lang="sass">
.edit-post
  margin: 40px auto
  width: 800px
</style>
