<template>
  <a
    :class="{'recommend-button': true, recommended}"
    href="#"
    @click.prevent="recommend"
    v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
    :title="recommended ? $t('Cancel recommendation') : $t('Recommend post')">
  </a>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'RecommnendButtonPost',

  props: {
    post: Object,
    recommended: Boolean,
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    async recommend() {
      const { author, slug } = this.post

      try {
        if (this.recommended) {
          await this.$axios.delete(`/recommendation/post/${author.id}/${slug}`)
          this.showSuccess(this.$t('Recommendation canceled'))
          this.$emit('update:recommended', false)
        } else {
          await this.$axios.post(`/recommendation/post/${author.id}/${slug}`)
          this.showSuccess(this.$t('Post recommended'))
          this.$emit('update:recommended', true)
        }
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

  &.recommended
    background: #444
    color: #eee
</style>
