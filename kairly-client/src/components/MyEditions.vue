<template>
  <my-editions-view>
    <h1>My Subscription</h1>
    <div>
      <MyEditionsItem
        v-for="edition in editions"
        :key="edition.id"
        v-bind:edition="edition"
      />
    </div>

  </my-editions-view>
</template>

<script>
import * as api from '@/api'
import { mapState, mapGetters } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'MyEditions',

  components: {
    MyEditionsItem
  },

  computed: {
    ...mapGetters({
      editions: 'allEditions'
    })
  },

  created() {
    this.$store.dispatch('getEditions')
  }
}
</script>

<style lang="sass">
my-editions-view
  display: block
  max-width: 900px
  margin: $baseline auto

  @media (max-width: $mobile)
    padding: 0 $baseline

  //- wrapper
  > div
    display: flex
    flex-wrap: wrap
    margin: 0 -$baseline/4

  //- heading
  h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-2  
</style>
