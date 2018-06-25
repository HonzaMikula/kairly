  <template>
  <my-editions-view>
    <EditionWidget
      v-for="edition in editions"
      :key="edition.id"
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

  components: {
    EditionWidget
  },

  computed: {
    ...mapGetters({
      editions: 'subscribedEditions'
    })
  },

  created() {
    this.$store.dispatch('getUserEditions')
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
</style>
