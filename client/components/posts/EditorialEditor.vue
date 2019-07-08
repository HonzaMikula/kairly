<template>
  <div class="editorial-post--editorial editor">
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
          <button>Save</button>
        </section>
      </header>

      <div class="content">
        <input type="text" placeholder="Title"/>
        <medium-editor v-model="content" :options="options" />
      </div>
    </article>
  </div>
</template>



<script>

export default {
  name: 'EditorialTweets',

  data() {
    return {
      content: '',
      options: {
        placeholder: {text: 'Content', hideOnClick: false},
      },
    }
  }

}
</script>
<style lang="sass">
.editorial-post--editorial.editor
  display: flex
  height: 100%

  > article
    display: flex
    flex-direction: column
    width: 100%

    .content
      display: flex
      flex-direction: column
      flex: 1

      > div
        flex: 1
</style>
