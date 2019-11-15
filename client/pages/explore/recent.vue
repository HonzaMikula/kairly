<template>
  <main class="explore--recent">
    <div class="explore--top-newspapers">
      <h2>{{ $t('Recent Issues') }}</h2>

      <div>
        <IssueWidget
          v-for="issue in issues"
          :key="`${issue.newspaper.fullName}#${issue.number}`"
          :issue="issue"
        />
      </div>

    </div>

    <section class="explore-recent">
      <h2>{{ $t('Recent Posts') }}</h2>

      <PostWrapper
        v-for="post in posts"
        :post="post"
        :isSubscribed="true"
        :key="post.id"
      />
    </section>

    <portal to="explore-header">{{ $t('Most Recent') }}</portal>

  </main>
</template>

<script>
import IssueWidget from '@/components/widgets/IssueWidget'
import PostWrapper from '@/components/PostWrapper'

export default {
  name: 'ExploreRecentTab',

  //auth: false,

  components: {
    IssueWidget,
    PostWrapper
  },

  head() {
    return {
      title: this.$t('Most Recent – Explore – Kairly')
    }
  },

  async asyncData({ app }) {
    const [issues, posts] = await Promise.all([
      app.$axios.$get('/recent/issues?count=3'),
      app.$axios.$get('/recent/posts')
    ])
    return { issues, posts }
  }
}
</script>

<style lang="sass">

main.explore--recent
  display: grid
  max-width: 900px
  margin: $baseline/2 auto
  grid-column-gap: $baseline
  grid-row-gap: $baseline
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto auto
  grid-template-areas: "explore-top-newspapers explore-top-newspapers" "explore-recent explore-recent"

  @media (max-width: $mobile)
    padding: 0 $baseline/4
    grid-template-columns: 100%
    grid-template-areas: "explore-top-newspapers" "explore-recent"

  section
    > h2
      font-size: $fs-2
      font-weight: 600
      line-height: $baseline * 2

    &.explore-0
      grid-area: explore-0

    &.explore-1
      grid-area: explore-1

    &.explore-2
      grid-area: explore-2

    &.explore-3
      grid-area: explore-3

    &.explore-recent
      grid-area: explore-recent

  .explore--top-newspapers
    grid-area: explore-top-newspapers

    > h2
      font-size: $fs-2
      font-weight: 600
      line-height: $baseline * 2

    //-- wrapper
    > div
      display: grid
      grid-row-gap: $baseline
      grid-template-columns: 1fr 1fr 1fr
      grid-column-gap: $baseline / 2

      @media (max-width: $mobile)
        grid-column-gap: $baseline / 4
        overflow-x: auto
        -webkit-overflow-scrolling: touch

        .newspaper-widget-view,
        .issue-widget-view
          min-width: 200px
</style>
