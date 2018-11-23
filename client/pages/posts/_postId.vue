<template>
  <app-layout>
    <div class="edit-post">
      <edit-article v-if="post.type == 'newspaper'" :post="post" buttonTitle="Save" @submit="savePost" />
      <edit-tweet v-if="post.type == 'tweet'" :post="post" buttonTitle="Save" @submit="savePost" />
    </div>
  </app-layout>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import EditArticle from '@/components/editor/EditArticle'
import EditTweet from '@/components/editor/EditTweet'

export default {
  name: 'Posts',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
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

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/')
      return
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
