<template>
  <IssueWidget
    :issue="post.ref"
  />
</template>

<script>
import post from './post';

export default {
  name: 'post-recommendation-issue',

  props: ["post", "isSubscribed"],

  components: {
    IssueWidget: () => import('@/components/widgets/IssueWidget')
  }
}
</script>

<style lang="sass">
</style>
