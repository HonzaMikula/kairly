<template>
  <div style="border: 1px solid gray">
    ❤❤❤ Recommendations ❤❤❤

    <component
      v-for="child in post.posts"
      :is="'post-' + child.type"
      :post="child"
      :isSubscribed="isSubscribed"
      :key="child.id"
    />
  </div>
</template>

<script>
import postRecommendationPost from '@/components/posts/recommendationPost'
import postRecommendationIssue from '@/components/posts/recommendationIssue'

export default {
  name: 'post-recommendations',

  props: ["post", "isSubscribed"],

  components: {
    postRecommendationPost,
    postRecommendationIssue
  }
}
</script>

<style lang="sass">
</style>
