<template>
  <div class="editorial-post-editor">
    <article role="article" class="post newspaper editorial">
      <header>
        <picture>
          <nuxt-link :to="{name: 'author', params: {author: editor.id}}">
            <img
              :src="editor.picture"
              :alt="editor.name"
            />
          </nuxt-link>
        </picture>
        <h3>
          <nuxt-link :to="{name: 'author', params: {author: editor.id}}">
            {{ editor.name }}<span v-if="editor.medium">, {{editor.medium}}</span>
          </nuxt-link>
        </h3>
        <section>
          <button
            class="save"
            @click="saveEditorial"
          >{{ $t('Save') }}</button>
        </section>
      </header>

      <div class="editorial-post-editor--content">
        <input
          v-model="title"
          type="text"
          :placeholder="$t('Title')"
        />
        <rich-editor
          v-model="content"
          :options="options"
        />
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: 'EditorialArticleEditor',

  props: {
    editorial: Object,
    newspaper: Object,
  },

  data() {
    return {
      title: this.editorial ? this.editorial.title : '',
      content: this.editorial ? this.editorial.content : '',
      options: {
        placeholder: this.$t('Editorial'),
      },
      editor: this.editorial ? this.editorial.author : this.$store.state.auth.user
    }
  },

  methods: {
    saveEditorial() {
      this.$emit('save', {
        type: 'article',
        title: this.title,
         content: this.content,
      })
    }
  }

}
</script>
<style lang="sass">
@import './styles/components/article-perex'

//- Editorial Post Editor
.editorial-post-editor
  display: flex
  height: 100%

  > article
    display: flex
    flex-direction: column
    width: 100%

    background: #f5f5f5

    header section .save
      margin-left: auto

//- Content
.editorial-post-editor--content
  display: flex
  flex-direction: column
  flex: 1

  //- title
  > input
    margin-bottom: $baseline / 2
    padding: 0

    border: 0
    background: #f5f5f5

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600
    line-height: 1.58


  //- medium editor
  .medium-editor-wrapper
    flex: 1
    min-height: $baseline * 3

    background: #f5f5f5

    line-height: 1.58
    hyphens: auto

    +article-perex

</style>
