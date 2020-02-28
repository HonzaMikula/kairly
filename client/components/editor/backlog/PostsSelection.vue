<template>
  <div class="posts-selection-view">
    <header>
      <h2>{{ $t('Select tweets') }}</h2>

      <button @click="$emit('done')">{{ $t('Done') }}</button>
    </header>

    <main>
      <!-- work with raw post in add / remove event -->
      <PostWrapper v-for="{post, source} in posts" :post="post" :key="post.id">
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
import Vue from "vue";

import { mapActions, mapMutations } from "vuex";
import PostWrapper from "@/components/PostWrapper";

export default {
  name: "PostsSelection",

  components: {
    PostWrapper
  },

  props: {
    newspaper: Object,
    selected: Array
  },

  data() {
    const {
      considered,
      next,
      upcoming,
      $posts
    } = this.$store.state.backlog.newspaperBacklog[this.newspaper.fullName];
    const posts = [];
    [considered, next, upcoming].forEach(bl => {
      bl.layout
        .filter(post => post.type === "post")
        .map(post =>
          this.$store.getters["entities/denormalize"]($posts[post.id], "Post")
        )
        //.filter(post => post.type === 'tweet')
        .forEach(post => posts.push({ post, source: bl.name }));
    });

    return {
      initialPosts: posts
    };
  },

  computed: {
    posts() {
      const ids = {};
      const posts = [];
      this.initialPosts.forEach(p => {
        ids[p.post.id] = true;
        posts.push(p);
      });

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
          .filter(post => post.type === "post" && !ids[post.id])
          .map(post =>
            this.$store.getters["entities/denormalize"]($posts[post.id], "Post")
          )
          //.filter(post => post.type === 'tweet')
          .forEach(post => posts.push({ post, source: bl.name }));
      });
      return posts;
    }
  },

  methods: {
    add(post, source) {
      this.$emit("add", { post, source });
    },

    remove(post, source) {
      this.$emit("remove", { post, source });
    }
  }
};
</script>

<style lang="sass">
@import './styles/components/buttons'

.posts-selection-view
  position: fixed
  right: $baseline
  top: 10vh
  z-index: 2

  display: grid
  grid-template-rows: $baseline * 1.5 1fr
  max-height: 80vh
  overflow: auto
  width: 300px

  background: #fff
  box-shadow: 0 0 7px rgba(0,0,0,0.5)

  @media (max-width: 1500px)
    right: 50%
    transform: translateX(45%)

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

    .post-body--content
      columns: 1

</style>
