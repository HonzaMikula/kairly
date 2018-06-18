<template>
  <div class="dev-backlog">
      <h2>Backlog</h2>
      <div class="backlog-content">
        <div>
          <h3>Post</h3>

          <div v-for="post in backlog" class="backlog-post">
            <!-- TODO use Post component which show correctly also tweets -->
            {{ post.id }} : {{ post.content.title }}

            <a href="#" @click.prevent="publish(post)">Publish &gt;&gt;&gt;</a>
          </div>

        </div>
        <div>
          <h3>Next Edition Issue</h3>

          <div v-for="post in published" class="backlog-post">
            <!-- TODO use Post component which show correctly also tweets -->
            {{ post.id }} : {{ post.content.title }}

            <a href="#" @click.prevent="undoPublish(post)">Return to backlog &lt;&lt;&lt;</a>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'EditionBacklog',

  components: {

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
    api.getEditionBacklog(this.edition.id).then(resp => {
      this.backlog = resp.backlog
      this.published = resp.publish
    })
  }
}
</script>

<style lang="sass">
.dev-backlog
  display: block
  border: 1px dashed black

  h2
    border-bottom: 1px solid black

.backlog-content
  display: flex
  min-height: 50px

.backlog-content > div
  flex: 1

.backlog-content > div:first-child
  border-right:  1px solid gray

.backlog-post
  border: 1px solid black
  padding: 20px

</style>
