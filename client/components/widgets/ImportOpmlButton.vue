<template>
  <div class="import-opml-button">
    <label>
      {{ text }}
      <input ref type="file" accept=".opml" @change="importOpml($event)" hidden>
    </label>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'ImportOpmlButton',
  props: {
    text: String
  },

  methods: {
    ...mapMutations({
      showError: 'messages/error',
    }),

    importOpml(ev) {
      const f = event.target.files[0]
      const reader = new FileReader()
      const items = []

      reader.addEventListener('loadend', ev => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(reader.result, "application/xml");
        const outlines = doc.getElementsByTagName('outline');

        for (let i = 0; i < outlines.length; i++) {
          const outline = outlines[i]
          if (!outline.hasChildNodes()) {
            let title = outline.getAttribute('title')
            const xmlUrl  = outline.getAttribute('xmlUrl')
            const htmlUrl  = outline.getAttribute('htmlUrl')
            if (xmlUrl) {
              if (!title) {
                title = (htmlUrl || xmlUrl).replace('http://', '').replace('https://', '')
              }
              items.push({title, url: xmlUrl})
            }
          }
        }

        this.$ga.event({
          eventCategory: 'Onboarding / Exploring',
          eventAction: 'Upload OPML with RSS feeds',
          eventLabel: null,
          eventValue: items.length
        })

        if (items.length > 100) {
          this.showError('Too many items')
        } else if (items.length == 0) {
          this.showError('OPML is empty')
        } else {
          this.$emit('loaded', items)
        }
      })
      reader.addEventListener('error', ev => {
        this.showError(ev + "")
      })
      reader.readAsText(f)
    }
  },
}
</script>
