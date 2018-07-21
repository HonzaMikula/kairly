  <template>
  <my-editions-view>
    <EditionWidget
      v-for="edition in editions"
      :key="edition.fullName"
      :edition="edition"
    />
  </my-editions-view>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import EditionWidget from '@/components/widgets/EditionWidget'

export default {
  name: 'MyEditions',

  metaInfo: {
    title: 'My Subscription - Editions'
  },

  components: {
    EditionWidget
  },

  computed: {
    ...mapState({
      editionIds: state => Object.keys(state.subscriptions.editions)
    }),

    editions() {
      const editions = this.editionIds
        .map(id => this.$store.getters.edition(id))
        .filter(edition => edition !== undefined)
      editions.sort(({title: a}, {title: b}) => a < b ? -1 : (a > b ? 1 : 0))
      return editions
    }
  },

  created() {
    this.$store.dispatch('getEditions', this.editionIds)
  }
}
</script>

<style lang="sass">
my-editions-view
  display: grid
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr 1fr
  grid-column-gap: $baseline / 2
  grid-row-gap: $baseline / 2

  @media (max-width: $mobile)
    grid-template-columns: 1fr 1fr
    grid-column-gap: $baseline / 4
</style>
