<template>
  <AppLayout :name="$t('Write tweet')">
    <div class="write-tweet-view">
      <EditTweet :buttonTitle="$t('Save a draft')" @submit="createPost" />
    </div>
  </AppLayout>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import AppLayout from '@/components/layout/AppLayout'
import EditTweet from '@/components/editor/EditTweet'

export default {
  name: 'CreateTweet',

  head() {
    return {
      title: this.$t('My Posts – Kairly')
    }
  },

  components: {
    AppLayout,
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
.write-tweet-view
  max-width: 900px
  margin: $baseline auto
</style>
