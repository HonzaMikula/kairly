<template>
  <div class="consider-post-view" v-on-clickaway="closeDialog">
    <header>{{ $t('For which newspaper?') }}</header>

    <section>
      <ul>
        <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in containedIn}">
          <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'
import { directive as onClickaway } from '@/lib/vue-clickaway'

export default {
  name: 'ConsiderPost',
  props: {
    post: Object
  },

  directives: {
    onClickaway
  },

  computed: {
    ...mapState({
      backlog: state => state.backlog
    }),

    ...mapGetters(['userNewspapers']),

    containedIn() {
      return this.backlog ? ( this.backlog[this.post.id] || {} ) : {}
    }
  },

  methods: {
    closeDialog() {
      this.$emit('closeConsiderPostDialog')
      console.log('test 100')
    },

    toggle(newspaper, ev) {
      if (newspaper.fullName in this.containedIn) {
        this.removeFromBacklog({newspaper, post: this.post})
      } else {
        this.addToBacklog({newspaper, post: this.post})
      }
      document.activeElement.blur()
    },

    ...mapActions(['addToBacklog', 'removeFromBacklog'])
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
