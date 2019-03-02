<template>
  <a
    class="recommend-button"
    href="#"
    @click.prevent="recommend"
    v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
    :title="$t('Recommend post')">
  </a>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'RecommnendButton',

  props: {
    post: Object
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    async recommend() {
      const { author, slug } = this.post

      try {
        await this.$axios.post(`/recommendation/${author.id}/${slug}`)
        this.showSuccess('Post recommended')
      } catch (err) {
        if (err.response.status === 400) {
          this.showError(err.response.data.error)
        } else {
          this.showError((err + '') || 'Request failed')
        }
      }
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.recommend-button
  +button-icon($fa-var-star)

</style>
