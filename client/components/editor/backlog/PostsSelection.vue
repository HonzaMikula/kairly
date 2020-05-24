<template>
  <div class="posts-selection-view">
    <header>
      <h2>{{ $t('Select posts') }}</h2>

      <div class="post-selection--search">
        <input v-model.lazy="search" type="text" :placeholder="$t('Search post')">
      </div>

      <div class="post-selection--filter">
        <label>
          <input v-model="selectedSources" type="checkbox" value="upcoming">
          {{ $t('Upcoming') }}
        </label>
        <label>
          <input v-model="selectedSources" type="checkbox" value="considered">
          {{ $t('Backlog') }}
        </label>
      </div>

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
      initialPosts: posts,
      search: '',
      selectedSources: ['considered', 'upcoming']
    }
  },

  computed: {
    posts () {
      const ids = {}
      let posts = []
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

      // - filtering by source
      if (this.selectedSources.length > 0) {
        posts = posts.filter((post) => {
          return this.selectedSources.includes(post.source)
        })
      }

      // - filtering by search
      posts = posts.filter((post) => {
        if (this.search !== '') {
          const search = this.search.toLowerCase()
          if (post.post.content.title && post.post.content.title.toLowerCase().includes(search)) {
            return true
          } else if (post.post.author.name.toLowerCase().includes(search)) {
            return true
          } else if (post.post.author.id.includes(search)) {
            return true
          }
          return false
        }
        return true
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
    grid-template-columns: max-content min-content auto max-content
    grid-column-gap: $baseline / 2
    align-items: center
    padding: $baseline/4 $baseline/2

    border-bottom: 1px solid #eee

    @media (max-width: $mobile)
      background: #eee

    //- heading
    h2
      font-weight: 600

    //- search
    .post-selection--search input
      border: 1px solid #ddd

      font-size: $fs-0
      line-height: $baseline

    //- checboxes
    .post-selection--filter
      @media (max-width: $mobile)
        display: none

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
