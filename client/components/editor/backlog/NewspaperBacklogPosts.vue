<template>
  <div class="newspaper-editor-backlog-section">
    <header class="newspaper-editor-backlog--heading">
      <h2>{{ title }}</h2>

      <button @click="() => expanded = !expanded" :class="{'is-expanded': expanded}"></button>

      <p>{{ description }}</p>

    </header>

    <div
      v-show="expanded"
      class="newspaper-backlog--next-issue"
    >

      <div v-if="!backlog.length" class="no-post">
        <h2>{{ $t('No posts in backlog') }}</h2>
      </div>

      <NewspaperBacklogPost
        v-for="(log, idx) in backlog"
        :key="log.post.id"
        :newspaper="newspaper"
        :log="log"
        :canMoveUp="idx > 0 || source !== 'upcoming'"
        :canMoveDown="idx < backlog.length - 1 || source != 'considered'"
        :source="source"
      />
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions, mapMutations } from 'vuex'


import NewspaperBacklogPost from '@/components/editor/backlog/NewspaperBacklogPost'

export default {
  name: 'NewspaperBacklogPosts',

  components: {
    NewspaperBacklogPost,
  },

  data() {
    return {
      expanded: true,
    }
  },

  props: {
    newspaper: Object,
    title: String,
    description: String,
    backlog: Array,
    source: String,
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

.newspaper-editor-backlog-section
  margin-bottom: $baseline * 2

.newspaper-editor-backlog--heading
  display: grid
  grid-template-columns: $baseline*1.25 1fr auto 1fr $baseline*1.25
  grid-template-rows: auto auto
  grid-column-gap: $baseline / 2
  margin: $baseline 0 $baseline/2 0

  //- heading
  h2
    grid-column: 3

    font-family: $ff-serif
    font-size: $fs-2
    line-height: $baseline * 1.25

  //- expand button
  button
    +button-icon($fa-var-plus, icon, solid)
    grid-column: 1
    grid-row: 1
    background: #fafafa

    &.is-expanded
      +button-icon($fa-var-minus, icon, solid)
      background: #fafafa

  //- when issue will be published
  p
    grid-row: 2
    grid-column: 1 / span 5
    color: #999

    font-family: $ff-serif
    text-align: center

//- Next Issue
.newspaper-backlog--next-issue
  .no-post
    display: flex
    align-items: center
    justify-content: center
    flex-direction: column
    height: 100%
    max-height: 50vh

    color: #999

    &::before
      +fa-icon()
      @extend .fas

      display: block
      margin-bottom: $baseline

      font-size: $fs-4

      content: fa-content($fa-var-clock)

    h2
      margin-bottom: $baseline / 2

      font-size: $fs-4
      line-height: $baseline * 2
      text-align: center
</style>
