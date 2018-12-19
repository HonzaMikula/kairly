<template>
  <author-subscription-view>
    <a
      href=""
      @click.prevent="$refs.followWidget.openSubscribeWidget()"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :title="$t('Change the subscriptions')">

      <p
        v-if="frequency == '6x_per_day'"
        v-html="$t('Daily every <strong>3 hours</strong>')">
      </p>

      <p
        v-if="frequency == '3x_per_day'"
        v-html="$t('Daily at <strong>6:00</strong>, <strong>12:00</strong> and <strong>18:00</strong>')">
      </p>

      <p
        v-if="frequency == 'daily'"
        v-html="$t('Daily at <strong>{xTime}</strong>', {xTime: time})">
      </p>

      <p
        v-if="frequency == 'weekly'"
        v-html="$t('Weekly on <strong>{xDay}</strong> at <strong>{xTime}</strong>', { xDay: getDayOfWeekLabel(dow), xTime: time })">
      </p>
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
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
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

  mixins: [PeriodicityMixin],

  computed: {
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

    &:focus,
    &:hover
      color: #000
</style>
