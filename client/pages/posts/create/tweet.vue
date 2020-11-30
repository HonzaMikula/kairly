<template>
  <AppLayout :name="$t('Write tweet')">
    <div class="write-tweet-view">
      <EditTweet :button-title="$t('Save a draft')" @submit="createPost" />
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import EditTweet from '@/components/editor/EditTweet'

export default {
  name: 'CreateTweet',

  components: {
    AppLayout,
    EditTweet
  },

  head () {
    return {
      title: this.$t('Write a Tweet – Kairly')
    }
  },

  methods: {
    async createPost (data) {
      await this.$axios.$post('/drafts', data)
      this.$router.push('/posts')
    }
  }
}
</script>

<style lang="sass">
.write-tweet-view
  max-width: 900px
  margin: $baseline auto
</style>
