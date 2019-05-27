<template>
  <div class="import-rss-button">
    <label>
      {{ text }}
      <a href="" @click.prevent="onClick">Import RSS</a>
    </label>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'ImportRssButton',
  props: {
    text: String
  },

  methods: {
     ...mapMutations(['showError']),

    onClick(ev) {
        const url = window.prompt("Insert RSS link")
        if (!url) {
            return
        }

        const title = url.replace('http://', '').replace('https://', '')

        this.$store.commit('opml', [
           {title, xmlUrl: url, htmlUrl: url}
        ])
        this.$emit('loaded')
    },
  },
}
</script>
