<template>
  <editions-view>
    <editions-considered-posts>
      <h1>Considered Posts</h1>
      <draggable v-model="consideredPosts">
        <considered-post 
          v-for="consideredPost in consideredPosts"
          :key="consideredPost.id">
          <timeline-post--header v-on:mouseleave="closeAuthorWidget()">
            <img :src="consideredPost.author.picture" :alt="consideredPost.author.name" />
          
            <timeline-post--header--author>
              <span v-on:mouseover="openAuthorWidget()">{{ consideredPost.author.name }}, {{consideredPost.author.medium}}</span>
            </timeline-post--header--author>

            <cAuthorWidget 
              :post="consideredPost"
              v-if="isAuthorWidgetOpen"
              v-on:authorwidgetclose="closeAuthorWidget()">
            </cAuthorWidget>

            <timeline-post--header--info>
              {{ consideredPost.type }} • {{ consideredPost.time }}
              • <span class="responses">{{ consideredPost.favorites }}</span>
            </timeline-post--header--info>

            <timeline-post--header--action-buttons v-on-clickaway="closePostWidgets">
              <button-icon class="remove"
                v-tooltip.top="'Remove from Edition'">
              </button-icon>
            </timeline-post--header--action-buttons>
          </timeline-post--header>

          <consider-post--content>
            {{ consideredPost.content.title }}
          </consider-post--content>

          <consider-post--footer>
            <consider-post--footer--button>
              Put it to Edition
            </consider-post--footer--button>
          </consider-post--footer>
          
        </considered-post>
      </draggable>

    </editions-considered-posts>

    <editions-upcoming-edition>
      <editions-upcoming-edition--header>
        <h1>Your Upcoming Edition</h1>

        <button-with-icon role="button">Publish</button-with-icon>
      </editions-upcoming-edition--header>

      <editions-upcoming-edition--posts>
        
        <edition-upcoming-edition--post></edition-upcoming-edition--post>
        <edition-upcoming-edition--post></edition-upcoming-edition--post>
        <edition-upcoming-edition--post></edition-upcoming-edition--post>
        <edition-upcoming-edition--post></edition-upcoming-edition--post>
        <edition-upcoming-edition--post></edition-upcoming-edition--post>

      </editions-upcoming-edition--posts>
    </editions-upcoming-edition>
  </editions-view>
</template>

<script>
import consideredPosts from '@/data/consideredForEdition.json'
import draggable from 'vuedraggable'

export default {
  name: 'Editions',

  data: function () {
    return {
      consideredPosts
    }
  },

  components: {
    draggable
  },

  created: function () { 
    this.consideredPost = consideredPosts
    console.log(consideredPost)
  }
}
</script>