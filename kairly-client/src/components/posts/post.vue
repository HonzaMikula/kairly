<template>
  <timeline-post role="article" :class="post.type">
    <timeline-post--header v-on:mouseleave="closeAuthorWidget()">
      <router-link :to="post.author.url">
        <img :src="post.author.picture" :alt="post.author.name" />
      </router-link>

      <timeline-post--header--author>
        <router-link :to="post.author.url">
          {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </router-link>
      </timeline-post--header--author>

      <authorWidget
        :author="post.author"
        v-if="isAuthorWidgetOpen"
        v-on:authorwidgetclose="closeAuthorWidget()">
      </authorWidget>

      <timeline-post--header--info>
        {{ post.time | moment('calendar') }}
        • <span class="responses">{{ post.favorites }}</span>
      </timeline-post--header--info>
    </timeline-post--header>

    <slot></slot>
  </timeline-post>
</template>

<script>
import { directive as onClickaway } from 'vue-clickaway'
import AuthorWidget from '@/components/widgets/author'

export default {
  name: 'post',
  props: ["post", "isSubscribed"],
  directives: {
    onClickaway,
  },
  data: function () {
    return {
      isAuthorWidgetOpen: false,
      isReadLaterWidgetOpen: false,
      isEditionWidgetOpen: false,
      timer: null,
    }
  },
  methods: {
    openAuthorWidget() {
      this.timer = setTimeout(() => {
        this.isAuthorWidgetOpen = true;
        this.$forceUpdate();
      }, 500);
    },

    closeAuthorWidget() {
      clearTimeout(this.timer)
      if (this.isAuthorWidgetOpen) {
        this.isAuthorWidgetOpen = false
        this.$forceUpdate()
      }
    }
  },

  components: {
    AuthorWidget
  }
}
</script>
