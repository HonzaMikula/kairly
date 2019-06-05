<template>
  <a
    :class="{'recommend-button-issue': true, 'recommended': recommended}"
    href="#"
    @click.prevent="recommend"
    v-b-tooltip
    :title="$t('Recommend')"
    :aria-label="$t('Recommend')">
  </a>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'RecommnendButtonIssue',

  props: {
    issue: Object,
  },

  computed: {
    recommended() {
      return this.$store.state.recommendedIssues[this.issue.id] || false
    }
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess', 'recommendedIssue']),

    async recommend() {
      try {
        const { id } = this.issue
        if (this.recommended) {
          await this.$axios.delete(`/recommendation/issue/${id}`)
          this.recommendedIssue({id, value: false})
        } else {
          await this.$axios.post(`/recommendation/issue/${id}`)
          this.recommendedIssue({id, value: true})
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
