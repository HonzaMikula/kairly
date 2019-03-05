<template>
  <div>
    ❤❤❤ Recommennded Issue ❤❤❤

    <IssueWidget
      :issue="post.ref"
    />
  </div>
</template>

<script>
import post from './post';
import IssueWidget from '@/components/widgets/IssueWidget'

export default {
  name: 'post-recommendation-issue',

  props: ["post", "isSubscribed"],

  components: {
    IssueWidget
  }
}
</script>

<style lang="sass">
</style>
