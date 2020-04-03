<template>
  <a
    :class="{'recommend-button': true, recommended}"
    href="#"
    :aria-label="$t('Recommend')"
    @click.prevent="recommend"
  />
</template>

<script>
import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'RecommnendButtonPost',

  mixins: [ErrorHandler],

  props: {
    post: Object,
    recommended: Boolean,
  },

  methods: {
    async recommend () {
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
        this.handleError(err)
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
