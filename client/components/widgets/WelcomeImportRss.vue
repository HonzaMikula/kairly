<template>
  <div class="welcome--import--rss">
    <label>
      {{ $t('Import RSS feeds') }}
      <input ref type="file" accept=".opml" @change="importOpml($event)" hidden>
    </label>
    <p>{{ $t('Upload OPML file.') }}</p>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'WelcomeImportRss',

  methods: {
     ...mapMutations(['showError']),

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
              items.push({title, xmlUrl, htmlUrl})
            }
          }
        }
        if (items.length > 100) {
          this.showError('Too many items')
        } else if (items.length == 0) {
          this.showError('OPML is empty')
        } else {
          this.$store.commit('opml', items)
          this.$emit('loaded')
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


<style lang="sass">
//- Imports
@import './styles/components/buttons'

.welcome--import--rss
  label
    +button-icon($fa-var-rss, icon-text, solid)

</style>
