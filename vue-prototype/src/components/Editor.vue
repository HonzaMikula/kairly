<template>
  <editor-view>
    
    <editor-switcher>
      <editor-switcher--item class="is-active">Article</editor-switcher--item>
      <editor-switcher--item>Tweet</editor-switcher--item>
    </editor-switcher>

    <editor-title>
      <input type="text" placeholder="Title" />
    </editor-title>
      
    <editor-content>
      <vue-mce :config="config" />
    </editor-content>

    <editor-footer>
      <button-with-icon>Publish Post</button-with-icon>
    </editor-footer>

  </editor-view>
</template>

<script>

import { component } from 'vue-mce'

export default {
  name: 'Editor',

  components: {
    'vue-mce': component,
  },

  data: function () {
    return {
      config: {
        theme: 'inlite',
        plugins: 'image media table link paste contextmenu textpattern autolink codesample',
        insert_toolbar: 'quickimage quicktable media codesample',
        selection_toolbar: 'bold italic | quicklink h2 h3 blockquote',
        inline: true,
        paste_data_images: true,
      }
    }
  }

}
</script>