<template>
  <AppLayout :name="$t('Write article')">
    <div class="write-article-view">
      <EditArticle :buttonTitle="$t('Save a draft')" @submit="createPost" />
    </div>
  </AppLayout>
</template>


<script>
import { mapActions, mapState } from 'vuex'
import AppLayout from '@/components/layout/AppLayout'
import EditArticle from '@/components/editor/EditArticle'

export default {
  name: 'CreateArticle',

  head() {
    return {
      title: this.$t('Write an Article – Kairly')
    }
  },

  components: {
    AppLayout,
    EditArticle
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
.write-article-view
  max-width: 900px
  margin: $baseline auto
</style>
