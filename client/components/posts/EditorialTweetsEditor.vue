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
          <button @click="save()">Save</button>
        </section>
      </header>

      <div>
        TODO
      </div>
    </article>
  </div>
</template>

<script>

export default {
  name: 'EditorialTweetsEditor',

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
      this.$emit('save', {})
    }
  }

}
</script>
<style lang="sass">

</style>
