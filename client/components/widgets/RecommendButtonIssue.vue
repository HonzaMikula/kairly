<template>
  <button
    v-b-tooltip
    :class="{'recommend-button-issue': true, 'recommended': recommended}"
    :title="$t('Recommend')"
    :aria-label="$t('Recommend')"
    @click="recommend"
  />
</template>

<script>
import { mapMutations } from 'vuex'

import ErrorHandler from '@/mixins/ErrorHandler'

export default {
  name: 'RecommnendButtonIssue',

  mixins: [ErrorHandler],

  props: {
    issue: Object,
  },

  computed: {
    recommended () {
      return this.$store.state.recommendedIssues[this.issue.id] || false
    }
  },

  methods: {
    ...mapMutations(['recommendedIssue']),

    async recommend () {
      try {
        const { id } = this.issue
        if (this.recommended) {
          await this.$axios.delete(`/recommendation/issue/${id}`)
          this.recommendedIssue({ id, value: false })
        } else {
          await this.$axios.post(`/recommendation/issue/${id}`)
          this.recommendedIssue({ id, value: true })
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

.recommend-button-issue
  +button-icon($fa-var-star, icon-text)

  &.recommended
    background: $c-base
    color: #fff
</style>
