<template>
  <a
    :class="{'recommend-button-issue': true, recommended}"
    href="#"
    @click.prevent="recommend"
    v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
    :title="$t('Recommend')"
    :aria-label="$t('Recommend')">
  </a>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'RecommnendButtonPost',

  props: {
    issue: Object,
    recommended: Boolean,
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    async recommend() {
      try {
        if (this.recommended) {
          await this.$axios.delete(`/recommendation/issue/${this.issue.id}`)
          this.$emit('update:recommended', false)
        } else {
          await this.$axios.post(`/recommendation/issue/${this.issue.id}`)
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

.recommend-button-issue
  +button-icon($fa-var-star, icon-text)

  &.recommended
    background: $c-base
    color: #fff
</style>
