<template>
  <author-detail-view
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="loadingPosts"
    infinite-scroll-distance="100"
  >
    <loading-spinner v-if="loadingProfile"></loading-spinner>

    <div v-else>
      <author-detail--header>
        <picture>
          <img :src="author.picture" :alt="author.name"/>
        </picture>
        <h1>{{ author.name }}</h1>
        <p>{{ author.bio }}</p>
      </author-detail--header>

      <author-detail--subscribe>
        <button
          v-bind:class="{ 'is-subscribed': author.isSubscribed }"
          v-on:click="subscribe($event)"
        >{{ author.isSubscribed ? 'Unfollow author' : 'Follow author'}}</button>
      </author-detail--subscribe>

      <author-detail--editions v-if="editions.length">
        <h2>{{ author.name }}'s Editions</h2>

        <div>
          <MyEditionsItem
            v-for="edition in editions"
            :key="edition.id"
            v-bind:edition="edition"
          />
        </div>

        <button v-if="editionIds.length > 3" v-on:click="toggleEditions()">{{ !showAllEditions ? 'Show all editions' : 'Hide editions' }}</button>

      </author-detail--editions>

      <author-detail--posts v-if="posts.length">
        <h2>{{ author.name }}'s Posts</h2>

        <PostWrapper
          v-for="post in posts"
          :post="post"
          :isSubscribed="true"
          :key="post.id"
        />
      </author-detail--posts>

      <loading-spinner v-if="loadingPosts"></loading-spinner>
    </div>

  </author-detail-view>
</template>


<script>
import * as api from '@/api'

import MyEditionsItem from '@/components/MyEditionsItem'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'AuthorDetail',

  components: {
    MyEditionsItem,
    PostWrapper
  },

  data: function () {
    return {
      loadingProfile: true,
      loadingPosts: true,
      author: null,
      showAllEditions: false,
      editionIds: [],
      posts: [],
      cursor: null
    }
  },

  computed: {
    editions() {
      const ids = this.showAllEditions ? this.editionIds : this.editionIds.slice(0, 3)
      return ids.map(id => this.$store.getters.edition(id))
    }
  },

  methods: {
    subscribe(ev) {
      const value = !this.author.isSubscribed
      api.postAuthorSubsription(this.author, value).then(author => this.author)
      this.author.isSubscribed = value
      ev.target.blur()
    },

    toggleEditions() {
      this.showAllEditions = !this.showAllEditions
    },

    handlePostsData: function(resp) {
      resp.posts.forEach(post => this.posts.push(post))
      this.cursor = resp.cursor
      this.loadingPosts = false
    },

    loadMore() {
      if (this.cursor) {
        this.loadingPosts = true
        api.getAuthorPosts(this.$route.params.authorId, this.cursor).then(this.handlePostsData)
      }
    }
  },

  created() {
    api.getAuthorDetail(this.$route.params.authorId).then(resp => {
      resp.editions.forEach(e => this.$store.dispatch('editionUpdated', e))
      this.author = resp.author
      this.editionIds = resp.editions.map(e => e.id)
      this.loadingProfile = false
    })
    api.getAuthorPosts(this.$route.params.authorId, null).then(this.handlePostsData)
  }
}
</script>
