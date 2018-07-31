  <template>
  <my-editions-view>
    <my-editions--empty
      v-if="editions.length === 0">
      <h1>No newspapers</h1>
      <p>You haven't subscribe to any newspapers yet. On Explore page you can find newspapers you might like.</p>
      <router-link to="/explore">Explore newspapers</router-link>
    </my-editions--empty>

    <EditionWidget
      v-else
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
    title: 'Newspapers - My Subscription - Kairly'
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

my-editions--empty
  grid-column: 1 / span 3

  padding: $baseline

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  p
    margin-bottom: $baseline

  a
    +subscribed-button

    display: inline-block

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
