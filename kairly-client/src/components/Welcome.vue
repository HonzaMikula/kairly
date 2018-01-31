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
import { mapState } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'Welcome',
  components: {
    MyEditionsItem
  },
  computed: {
    ...mapState({
      editions: state => {
        const editions = (state.editions || []).filter(item => item.issues)
        if (editions.length > 3) {
          editions.splice(0, editions.length - 3)
        }
        return editions
      }
    })
  },
  created: function () {
    this.$store.dispatch('getEditions')
  }
}
</script>
