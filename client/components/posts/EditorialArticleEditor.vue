<template>
  <div class="editorial-post-editor">
    <article role="article" class="post newspaper editorial">
      <header>
        <picture>
          <a href="/janmikula" class="">
            <img src="https://cdn.kairly.com/media/users/janmikula.jpg" alt="Dojnice">
          </a>
        </picture>
        <h3>
          <a href="/janmikula" class="">Jan Mikula, editor</a>
        </h3>
        <section>
          <button @click="save()" class="save">Save</button>
        </section>
      </header>

      <div class="editorial-post-editor--content">
        <input
          v-model="title"
          type="text"
          placeholder="Title"
        />
        <medium-editor
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
    editorial: Object
  },

  data() {
    return {
      title: this.editorial ? this.editorial.title : '',
      content: this.editorial ? this.editorial.content : '',
      options: {
        placeholder: {text: 'Content', hideOnClick: false},
      },
    }
  },

  methods: {
    async save() {
      this.$emit('save', {
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
