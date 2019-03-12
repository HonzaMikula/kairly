<template>
  <a
    :class="{'recommend-button': true, recommended}"
    href="#"
    @click.prevent="recommend"
    :aria-label="$t('Recommend')">
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
          this.$emit('update:recommended', false)
          this.$ga.event({
            eventCategory: 'Unrecommend post',
            eventAction: author.name,
            eventLabel: slug
          })
        } else {
          await this.$axios.post(`/recommendation/post/${author.id}/${slug}`)
          this.$emit('update:recommended', true)
          this.$ga.event({
            eventCategory: 'Recommend post',
            eventAction: author.name,
            eventLabel: slug
          })
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
  +button-icon($fa-var-star, icon-text)

  &.recommended
    background: $c-base
    color: #fff
</style>
