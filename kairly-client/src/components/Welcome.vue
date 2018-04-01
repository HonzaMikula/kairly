<template>
  <timeline-welcome>
    <h1>Welcome to Kairly</h1>
    <p>Start with selecting editions you want to subscribe.</p>

    <timeline-welcome--my-editions>
      <MyEditionsItem
        v-for="edition in editions"
        :key="edition.id"
        v-bind:edition="edition"
      />
    </timeline-welcome--my-editions>

    <timeline-welcome--more-editions>
      <router-link to='/my-editions'>View more editions</router-link>
      <br />
      <!-- TODO remove reload hack, instead trigger timeline load -->
      <button v-on:click="$router.go({ name: '/' })">Show me editions</button>
    </timeline-welcome--more-editions>
  </timeline-welcome>
</template>

<script>
import * as api from '@/api'
import { mapGetters } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'Welcome',

  components: {
    MyEditionsItem
  },

  computed: {
    ...mapGetters(['allEditions']),

    editions() {
      return (this.allEditions || []).slice(0, 3)
    }
  },

  created() {
    this.$store.dispatch('getEditions')
  }
}
</script>
