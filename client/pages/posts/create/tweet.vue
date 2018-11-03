<template>
  <div>
    Tweet
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

//import EditArticle from '@/components/editor/EditArticle'

export default {
  name: 'Posts',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
    }
  },

  components: {
  },

  // methods: {
  //   async createPost(data) {
  //     const { post } = await this.$axios.$post(`/drafts`, data)
  //     this.$router.push("/posts")
  //   }
  // },

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
