<template>
  <author-detail-view>
    <loading-spinner v-if="loading"></loading-spinner>

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

        <button v-if="allEditions.length > 3" v-on:click="toggleEditions()">{{ !isAllEditionsOpened ? 'Show all editions' : 'Hide editions' }}</button>

      </author-detail--editions>

      <author-detail--posts v-if="posts.length">
        <h2>{{ author.name }}'s Posts</h2>

        <PostWrapper
          v-for="post in posts"
          :post="post"
          :isSubscribed="author.isSubscribed"
          :key="post.id"
        />
      </author-detail--posts>
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
      'loading': true,
      'author': null,
      'isAllEditionsOpened': false,
      'ellEditions': [],
      'topEditions': [],
      'editions': [],
      'posts': []
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
      if (!this.isAllEditionsOpened)
        this.editions = this.allEditions
      else
        this.editions = this.topEditions 

      this.isAllEditionsOpened = !this.isAllEditionsOpened  
    }
  },

  created() {
    api.getAuthorDetail(this.$route.params.authorId).then(resp => {
      this.author = resp.author
      this.allEditions = resp.editions
      this.topEditions = resp.editions.slice(0, 3)
      this.posts = resp.posts
      this.editions = this.topEditions
      this.loading = false
    })
  }
}
</script>
