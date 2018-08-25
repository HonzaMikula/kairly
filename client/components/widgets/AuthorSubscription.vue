<template>
  <author-subscription-view>
    <a
      href=""
      v-on:click.prevent="$refs.followWidget.openSubscribeWidget()"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      title="Change the subscription">
      <template v-if="frequency == '3x_per_day'">
        Daily at <strong>6:00</strong>,
        <strong>12:00</strong> and <strong>18:00</strong>
      </template>

      <template v-if="frequency == 'daily'">
        Daily at <strong>{{ time }}</strong>
      </template>

      <template v-if="frequency == 'weekly'">
        Weekly on <strong>{{ DAYS[dow - 1] }}</strong> at <strong>{{ time }}</strong>
      </template>
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


export default {
  name: 'AuthorSubscription',

  props: {
    author: Object,
    subscription: Object
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
    frequency() { return this.subscription && this.subscription.frequency },
    dow() { return this.subscription && this.subscription.dow },
    time() { return this.subscription && this.subscription.time }
  },

  methods: {
    follow(periodicity) {
      this.$store.dispatch('subscribeAuthor', {
        authorId: this.author.id,
        periodicity
      })
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

    &:focus,
    &:hover
      color: #000
</style>
