<template>
  <AppLayout :name="$t('Write article')">
    <div class="write-article-view">
      <EditArticle :button-title="$t('Save a draft')" @submit="createPost" />
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import EditArticle from '@/components/editor/EditArticle'

export default {
  name: 'CreateArticle',

  components: {
    AppLayout,
    EditArticle
  },

  head () {
    return {
      title: this.$t('Write an Article – Kairly')
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
.write-article-view
  max-width: 900px
  margin: $baseline auto
</style>
