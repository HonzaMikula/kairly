<template>
  <div v-if="managedEditions">
    <a href="#" @click.prevent="showEditions = true">Add to backlog</a>
    <div v-if="showEditions">
      <div v-for="ed in managedEditions">
        <span v-show="backlog[ed.id]">✓</span>
        <a href="#" @click.prevent="add(ed)">{{ ed.title }}</a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import * as api from '@/api'

export default {
  name: 'BacklogAdd',
  props: {
    post: Object
  },

  data() {
    return {
      showEditions: false,
      backlog: {} // TODO provide initial state
    }
  },

  computed: mapState({
    managedEditions: state => state.managedEditions
  }),

  methods: {
    add(edition) {
      api.addToBacklog(edition.id, this.post.id)
      .then(() => {
        this.backlog = {...this.backlog, [edition.id]: true}
      })
    }
  }
}
</script>

<style lang="sass">
</style>
