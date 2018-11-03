<template>
  <my-posts>
    Published post
  </my-posts>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import MyPosts from '@/components/layout/MyPosts'

export default {
  name: 'Drafts',

  components: {
    MyPosts,
  },

  computed: {
    ...mapState({
      user: state => state.auth.user
    })
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
