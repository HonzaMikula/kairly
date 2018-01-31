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
import { mapState } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'MyEditions',
  components: {
    MyEditionsItem
  },
  computed: {
    ...mapState({
      editions: state => state.editions || []
    })
  },
  created: function () {
    this.$store.dispatch('getEditions')
  }
}
</script>
