<template>
  <app-layout>
    <div>
      <edit-post buttonTitle="Save a draft" @submit="createPost" />
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
    async createPost(data) {
      const { post } = await this.$axios.$post(`/drafts`, data)
      this.$router.push("/posts")
    }
  },

  async fetch({ store, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }
  }
}
</script>

<style lang="sass">
</style>
