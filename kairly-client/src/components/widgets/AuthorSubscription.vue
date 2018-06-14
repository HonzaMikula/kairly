<template>
  <author-subscription-view>
    <a href="" v-on:click.prevent="$refs.followWidget.openSubscribeWidget()" v-if="period == '3x_per_day'">
      Daily at <strong>6:00</strong>, 
      <strong>12:00</strong> and <strong>18:00</strong>
    </a>

    <a href="" v-on:click.prevent="$refs.followWidget.openSubscribeWidget()" v-else-if="period == 'daily'">
      Daily at <strong>{{ time }}</strong>
    </a>

    <a href="" v-on:click.prevent="$refs.followWidget.openSubscribeWidget()" v-else-if="period == 'weekly'">
      Weekly on <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>
    </a>

    <follow-author
      ref="followWidget"
      :author="author"
      :onSelect="follow"
      :cancelingSubscription="true"
    />
  </author-subscription-view>
</template>

<script>
import FollowAuthor from '@/components/widgets/FollowAuthor'
import * as api from '@/api'

export default {
  name: 'AuthorSubscription',
  props: {
    'author': Object
  },

  components: {
    FollowAuthor
  },

  data() {
    return {
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: {
    period() { return this.author.subscription && this.author.subscription.period },
    dow() { return this.author.subscription && this.author.subscription.dow },
    time() { return this.author.subscription && this.author.subscription.time }
  },

  methods: {
    follow(period, time, dow) {
      // TODO split handlers
      this.$store.dispatch('invalidateTimeline')
      api.subscribeAuthor(this.author, period, time, dow).then(author => this.author)
      this.author.subscription = { period, time, dow }
    }
  }
}
</script>

<style lang="sass">
author-subscription-view
  display: block

  font-size: $fs--2

  a
    color: #333

    text-decoration: none

    &:focus,
    &:hover
      color: #000
</style>
