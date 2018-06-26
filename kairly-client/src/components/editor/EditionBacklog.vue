<template>
  <edition-backlog-view>

    <edition-backlog--backlog>
      <div v-if="backlog.length == 0">no posts</div>

      <div v-for="post in backlog" class="backlog-post" :key="post.id">
        <h3>{{ post.content.title }}</h3>

        <p>
          <a href="#" @click.prevent="publish(post)">Publish</a>
        </p>
      </div>
    </edition-backlog--backlog>

    <edition-backlog--next-issue>
      <PostWrapper
        v-for="post in published"
        :post="post"
        :isSubscribed="true"
        :key="post.id"
      >
        <template slot="controls">
          <button-icon
            class="remove" aria-label="Remove from issue"
            v-tooltip.left="'Remove from issue'"
            @click.prevent="undoPublish(post)">
          </button-icon>
        </template>
      </PostWrapper>
    </edition-backlog--next-issue>
  </edition-backlog-view>
</template>

<script>
import * as api from '@/api'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'EditionBacklog',

  components: {
    PostWrapper
  },

  props: {
    edition: Object
  },

  data() {
    return {
      backlog: [],
      published: []
    }
  },

  methods: {
    init() {
      api.getEditionBacklog(this.edition.id).then(resp => {
        this.backlog = resp.backlog
        this.published = resp.publish
      })
    },

    publish(post) {
      api.addToBacklog(this.edition.id, post.id, true)
      .then(() => {
        this.backlog.splice(this.backlog.indexOf(post), 1)
        this.published.push(post)
      })
    },

    undoPublish(post) {
      api.addToBacklog(this.edition.id, post.id, false)
      .then(() => {
        this.published.splice(this.published.indexOf(post), 1)
        this.backlog.push(post)
      })
    }
  },

  created() {
    this.init()

    this.$watch('edition', edition => {
      this.init()
    })
  }
}
</script>

<style lang="sass">
edition-backlog-view
  display: grid
  grid-template-columns: auto 970px
  grid-column-gap: $baseline


//- Backlog
edition-backlog--backlog

  //- post
  > div
    padding: $baseline / 4
    margin-bottom: $baseline / 2
    background: #fff

  h3
    font-weight: 600

  p
    text-align: center

  a
    +subscribe-button

</style>
