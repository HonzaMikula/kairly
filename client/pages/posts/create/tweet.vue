<template>
  <div>
    <EditTweet :buttonTitle="$t('Save a draft')" @submit="createPost" />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import EditTweet from '@/components/editor/EditTweet'

export default {
  name: 'CreateTweet',

  head() {
    return {
      title: this.$t('My Posts – Kairly')
    }
  },

  components: {
    EditTweet
  },

  methods: {
    async createPost(data) {
      const { post } = await this.$axios.$post(`/drafts`, data)
      this.$router.push("/posts")
    }
  }
}
</script>

<style lang="sass">
</style>
