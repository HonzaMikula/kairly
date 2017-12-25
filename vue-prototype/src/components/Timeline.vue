<template>
  <timeline-view>
    <div v-for="edition in editionData.editions" :key="edition.id">
      <timeline-edition>
        <h1>{{edition.title}}</h1>

        <p>
          <timeline-edition--editor>
            <img v-if="edition.author.picture" :src="edition.author.picture" :alt="edition.author.name" /> 
            {{edition.author.name}}
          </timeline-edition--editor>
          •
          {{ edition.edition }}
          •
          {{edition.time}}
        </p>
      </timeline-edition>

      <component 
        v-for="post in postsInEdition[edition.postsId]"
        :is="post.testType"
        :post="post"
        :key="post.id"
        v-on:readlater="readLaterMessage()">
      </component>

    </div>
  </timeline-view>
</template>

<script>
import editionData from '@/data/editions.json'
import timelineData from '@/data/timeline.json'
import politicoEdtionData from '@/data/politicoEdition.json'
import cnnEdtionData from '@/data/cnnEdition.json'
import hnEdtionData from '@/data/hnEdition.json'
import newYorkTimeEditionData from '@/data/newYorkTimesEdition.json'

import postArticle from '@/components/posts/article'
import postBlog from '@/components/posts/blog'
import postNewspaper from '@/components/posts/newspaper'
import postTweet from '@/components/posts/tweet'
import postPicture from '@/components/posts/picture'

export default {
  name: 'Timeline',

  data: function () {
    return {
      editionData,
      timelineData,
      postsInEdition: [],
    }
  },

  components: {
    postArticle,
    postBlog,
    postNewspaper,
    postTweet,
    postPicture
  },

  created: function () {
    this.postsInEdition[1] = politicoEdtionData
    this.postsInEdition[2] = cnnEdtionData
    this.postsInEdition[3] = hnEdtionData
    this.postsInEdition[5] = newYorkTimeEditionData
  }
}
</script>