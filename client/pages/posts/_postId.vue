<template>
  <app-layout>
    <div style="margin: 40px auto; width: 800px">
      <edit-post :post="post" buttonTitle="Save" @submit="savePost" />
    </div>
  </app-layout>
</template>


<script>


import { mapActions, mapState } from 'vuex'

import AppLayout from '@/components/layout/AppLayout'
import EditPost from '@/components/editor/EditPost'

export default {
  name: 'Posts',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
    }
  },

  components: {
    AppLayout,
    EditPost
  },

  methods: {
    async savePost(data) {
      const { post } = await this.$axios.$patch(`/drafts/${this.post.id}`, data)
      this.$router.push("/posts")
    }
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
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
</style>
