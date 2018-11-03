<template>
  <div>
    <edit-article buttonTitle="Save a draft" @submit="createPost" />
  </div>
</template>


<script>
import { mapActions, mapState } from 'vuex'

import EditArticle from '@/components/editor/EditArticle'

export default {
  name: 'CreateArticle',

  metaInfo() {
    return {
      title: 'My Posts – Kairly'
    }
  },

  components: {
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
</style>
