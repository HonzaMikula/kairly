<template>
 <div>
   <ExploreTimeline :category="currentCategory" :period="currentPeriod" />
 </div>
</template>

<script>
import TABS from '@/exploreTabs'
import ExploreTimeline from '@/components/ExploreTimeline'

export default {
  name: 'ExploreTab',

  auth: false,

  components: {
    ExploreTimeline
  },

  head() {
    const title = this.currentCategory[this.$i18n.locale || 'en']
    return {
      title:  `${title} – ${this.$t('Explore')} – Kairly`
    }
  },

  data() {
    return {
      tabs: TABS,
      currentCategory: TABS.find(t => t.slug === this.$route.params.tab),
      currentPeriod: this.$route.params.date
    }
  }
}
</script>
