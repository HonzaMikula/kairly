<template>
  <author-subscription-view>
    <a
      href=""
      v-on:click.prevent="$refs.followWidget.openSubscribeWidget()"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :class="{'is-canceled': canceled}"
      :title="'Change the subscriptions'+ (canceled ? ' (is canceled)': '')">

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
      :subscription="subscription"
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
    canceled() { return this.subscription && !this.subscription.renewal},
    frequency() { return this.subscription && this.subscription.periodicity.frequency },
    dow() { return this.subscription && this.subscription.periodicity.dow },
    time() { return this.subscription && this.subscription.periodicity.time }
  }
}
</script>

<style lang="sass">
author-subscription-view
  display: block

  font-size: $fs--1

  a
    color: #555

    &.is-canceled::before
      +fa-icon()

      content: $fa-var-times-circle-o


    &:focus,
    &:hover
      color: #000
</style>
