<template>
  <timeline-post role="article">
      <timeline-post--header v-on:mouseleave="closeAuthorWidget()">
        <img :src="post.author.picture" :alt="post.author.name" />

        <timeline-post--header--author>
          {{ post.author.name }}<span v-if="post.author.medium">, {{post.author.medium}}</span>
        </timeline-post--header--author>

        <cAuthorWidget
          :author="post.author"
          v-if="isAuthorWidgetOpen"
          v-on:authorwidgetclose="closeAuthorWidget()">
        </cAuthorWidget>

        <timeline-post--header--info>
          {{ post.time | moment('calendar') }}
          • <span class="responses">{{ post.favorites }}</span>
        </timeline-post--header--info>

        <!--timeline-post--header--action-buttons v-on-clickaway="closePostWidgets">
          <button-icon class="edition"
            v-tooltip.top="'Consider for Edition'">
          </button-icon>
          <button-icon class="read-later"
            v-bind:class="{ 'is-active': isReadLaterActive }"
            v-tooltip.top="'Read it later'"
            v-on:click="openReadLaterWidget()">
          </button-icon>

          <cReadLaterWidget
            v-if="isReadLaterWidgetOpen"
            v-on:readlaterwidgetclose="closeReadLaterWidget()">
          </cReadLaterWidget>

          <cEditionWidget
            v-if="isEditionWidgetOpen"
            v-on:editionwidgetclose="closeEditionWidget()">
          </cEditionWidget>
        </timeline-post--header--action-buttons -->
      </timeline-post--header>

      <slot></slot>
    </timeline-post>
</template>

<script>
import { directive as onClickaway } from 'vue-clickaway'
import cAuthorWidget from './cAuthorWidget'
import cReadLaterWidget from './cReadLaterWidget'

export default {
  name: 'post',
  props: ["post", "isSubscribed"],
  directives: {
    onClickaway: onClickaway,
  },
  data: function () {
    return {
      isAuthorWidgetOpen: false,
      isReadLaterWidgetOpen: false,
      isEditionWidgetOpen: false,
      timer: null,
      isReadLaterActive: false
    }
  },
  methods: {

    openAuthorWidget: function () {
      var x = this;
      this.timer = setTimeout(function() {
        x.isAuthorWidgetOpen = true;
        x.$forceUpdate();
      }, 500);
    },

    closeAuthorWidget: function () {
      clearTimeout(this.timer)
      if (this.isAuthorWidgetOpen) {
        this.isAuthorWidgetOpen = false
        this.$forceUpdate()
      }
    },

    openReadLaterWidget: function () {
      this.isReadLaterActive = true
      this.isReadLaterWidgetOpen = true
      this.$forceUpdate()
    },

    closeReadLaterWidget: function () {
      if (this.isReadLaterWidgetOpen) {
        this.isReadLaterWidgetOpen = false
        this.$forceUpdate()
      }
    },

    closePostWidgets: function () {
      this.closeReadLaterWidget()
      this.closeEditionWidget()
    }
  },

  components: {
    cAuthorWidget,
    cReadLaterWidget
  }
}
</script>
