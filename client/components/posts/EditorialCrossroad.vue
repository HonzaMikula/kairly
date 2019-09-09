<template>
  <div class="editorial-post--editorial crossroad">
    <h2>Editorials</h2>
    <button @click="isTweetsSelectionOpened = !isTweetsSelectionOpened">Select tweets</button>
    <p>or</p>
    <button>Write editorial</button>

    <portal to="modal" v-if="isTweetsSelectionOpened">
      <TweetsSelection></TweetsSelection>
    </portal>
  </div>
</template>

<script>
import TweetsSelection from '@/components/editor/backlog/TweetsSelection'

export default {
  name: 'EditorialCrossroad',

  data() {
    return {
      isTweetsSelectionOpened: false
    }
  },

  props: {
    editorial: Object
  },

  components: {
    TweetsSelection
  }
}
</script>
<style lang="sass">
@import './styles/components/buttons'

//- Editorial Crossroad
.editorial-post--editorial.crossroad
  text-align: center

  h2
    margin-bottom: $baseline

    font-size: $fs-1
    font-weight: 600

  p
    margin: $baseline/2 0

  button
    +button(secondary, small)

</style>
