<template>
  <a
    class="recommend-button"
    href="#"
    @click.prevent="recommend"
    v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
    :title="$t('Recommend issue')">
  </a>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'RecommnendButtonPost',

  props: {
    issue: Object
  },

  methods: {
    ...mapMutations(['showError', 'showSuccess']),

    async recommend() {
      try {
        await this.$axios.post(`/recommendation/issue/${this.issue.id}`)
        this.showSuccess('Issue recommended')
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
