<template>
  <author-detail-view>
    <div v-if="loading">...</div>
    <div v-else>
      <author-detail--header>
        <picture>
          <img :src="author.picture" :alt="author.name"/>
        </picture>
        <h1>{{ author.name }}</h1>
        <p>{{ author.medium }}</p>
      </author-detail--header>

      <author-detail--subscribe>
        <button v-if="editions.length">Subscribe Editions</button>

        <button>Subscribe Posts</button>
      </author-detail--subscribe>

      <author-detail--editions v-if="editions.length">
        <h2>{{ author.name }}'s Editions</h2>

        <div style="display: flex">
          <MyEditionsItem
            v-for="edition in editions"
            :key="edition.id"
            v-bind:edition="edition"
          />
        </div>

      </author-detail--editions>

      <author-detail--posts>
        <h2>{{ author.name }}'s Posts</h2>

        <img src="../assets/kairly-temp-posts.png" />
      </author-detail--posts>
    </div>

  </author-detail-view>
</template>


<script>
import * as api from '@/api'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'AuthorDetail',

  components: {
    MyEditionsItem
  },

  data: function () {
    return {
      'loading': true,
      'author': null,
      'editions': null,
    }
  },

  created() {
    api.getAuthorDetail(this.$route.params.authorId).then(resp => {
      this.author = resp.author
      this.editions = resp.editions
      this.loading = false
    })
  }
}
</script>
