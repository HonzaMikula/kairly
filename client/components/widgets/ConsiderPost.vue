<template>
  <div v-on-clickaway="closeDialog" class="consider-post-view">
    <header>
      <h4>{{ $t('For which newspaper?') }}</h4>
      <strong
        v-b-tooltip
        class="consider-post--price"
        :title="$t('Article cost')"
      >
        <MoneyFormat :value="post.price" currency="Kč" />
      </strong>
    </header>

    <section>
      <ul>
        <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in postBacklog}">
          <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import MoneyFormat from '@/components/widgets/MoneyFormat'

export default {
  name: 'ConsiderPost',

  directives: {
    onClickaway
  },

  components: {
    MoneyFormat
  },

  props: {
    post: Object
  },

  computed: {
    ...mapState({
      backlog: state => state.backlog.userBacklog
    }),

    ...mapGetters(['userNewspapers']),

    postBacklog () {
      return this.backlog ? (this.backlog[this.post.id] || {}) : {}
    }
  },

  methods: {
    closeDialog () {
      this.$emit('closeConsiderPostDialog')
    },

    toggle (newspaper, ev) {
      const backlogName = this.postBacklog[newspaper.fullName]
      if (backlogName) {
        this.removeFromBacklog({
          newspaper,
          source: backlogName,
          post: this.post
        })
      } else {
        this.addToBacklog({
          newspaper,
          target: 'considered',
          post: this.post
        })
      }
      document.activeElement.blur()
    },

    ...mapActions({
      addToBacklog: 'backlog/add',
      removeFromBacklog: 'backlog/remove'
    })
  }
}
</script>

<style lang="sass">
@import './styles/components/context-menu'

.consider-post-view
  +context-menu

  position: absolute
  left: 50%

  top: 50px
  z-index: 10

  @media (max-width: 1120px)
    left: inherit
    right: -$baseline/4

    &::after
      left: inherit
      right: 5px

  //- header
  header
    display: flex
    padding: 0 $baseline/2

    h4
      margin-right: auto

  //- list
  li
    a::after
      content: fa-content($fa-var-check)
      transition: 0.15s opacity

    &.is-selected a::after
      opacity: 1 !important

      font-size: $fs-0
      content: fa-content($fa-var-check-circle)
      transition: 0.15s opacity

</style>
