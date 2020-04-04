<template>
  <div class="posts-selection-view">
    <header>
      <h2>{{ $t('Select tweets') }}</h2>

      <button @click="$emit('done')">{{ $t('Done') }}</button>
    </header>

    <main>
      <div class="posts-selection--external">
        <input type="url" :placeholder="$t('Paste URL')">
        <button>Add post</button>
      </div>
      <!-- work with raw post in add / remove event -->
      <PostWrapper v-for="{post, source} in posts" :key="post.id" :post="post">
        <template #global-controls>&nbsp;</template>
        <template #page-controls>
          <button v-if="selected.indexOf(post.id) === -1" class="add" @click="add(post, source)" />
          <button v-else class="remove" @click="remove(post, source)" />
        </template>
      </PostWrapper>
    </main>
  </div>
</template>

<script>
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'PostsSelection',

  components: {
    PostWrapper
  },

  props: {
    newspaper: { type: Object, required: true },
    selected: { type: Array, required: true }
  },

  data () {
    const {
      considered,
      next,
      upcoming,
      $posts
    } = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName]
    const posts = [];
    [considered, next, upcoming].forEach(bl => {
      bl.layout
        .filter(post => post.type === 'post')
        .map(post =>
          this.$store.getters['entities/denormalize']($posts[post.id], 'Post')
        )
        // .filter(post => post.type === 'tweet')
        .forEach(post => posts.push({ post, source: bl.name }))
    })

    return {
      initialPosts: posts
    }
  },

  computed: {
    posts () {
      const ids = {}
      const posts = []
      this.initialPosts.forEach(p => {
        ids[p.post.id] = true
        posts.push(p)
      })

      // do not remove from tweets when tweet is moved from baclog to editorial
      // but add tweet to list when moved from editoril back to backlog
      const {
        considered,
        next,
        upcoming,
        $posts
      } = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName];
      [considered, next, upcoming].forEach(bl => {
        bl.layout
          .filter(post => post.type === 'post' && !ids[post.id])
          .map(post =>
            this.$store.getters['entities/denormalize']($posts[post.id], 'Post')
          )
          // .filter(post => post.type === 'tweet')
          .forEach(post => posts.push({ post, source: bl.name }))
      })
      return posts
    }
  },

  methods: {
    add (post, source) {
      this.$emit('add', { post, source })
    },

    remove (post, source) {
      this.$emit('remove', { post, source })
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.posts-selection-view
  position: fixed
  right: 0
  top: 10vh
  z-index: 20

  display: grid
  grid-template-rows: $baseline * 1.5 1fr
  max-height: 90vh
  overflow: auto
  width: 900px

  background: #fff

  @media (max-width: $mobile)
    bottom: 0
    left: 0
    right: 0
    top: auto
    height: 60vh
    width: 100vw

    box-shadow: -2px -2px 4px #aaa

    transform: none

  //- Header
  > header
    display: grid
    grid-template-columns: auto min-content
    padding: $baseline/4 $baseline/2

    border-bottom: 1px solid #eee

    //- heading
    h2
      font-weight: 600

    //- done button
    button
      +button(primary, small)

  //- Main
  main
    overflow: auto

    @media (max-width: $mobile)
      .post-wrapper
        position: relative
        max-height: 250px
        overflow: hidden

        &::after
          position: absolute
          bottom: 0

          height: $baseline
          width: 100%

          background: linear-gradient(to bottom, transparent, #fff)

          content: ''

//- Add external article
.posts-selection--external
  display: flex
  margin: $baseline / 2

  @media (max-width: $mobile)
    margin: 0
    border-bottom: 1px solid #eee

  input
    box-sizing: border-box
    height: $baseline * 1.25
    padding: 0 $baseline/4
    width: 100%

    border: 1px solid #eee

    font-family: $ff-sans
    font-size: $fs--1
    line-height: 1.42

  button
    flex: 1
    border: 0

    background: #eee
    color: #555

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs--1
    line-height: 1.42
    white-space: nowrap

    &:hover,
    &:focus
      background: #ddd
      color: #000

</style>
