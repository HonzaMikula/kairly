<template>
  <backlog-add-view v-if="userNewspapers.length">
    <button-icon
      v-if="!showText"
      role="button"
      tabindex="0"
      aria-label="Consider for newspaper"
      v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
      :title="$t('Consider for newspaper')"
      @click.prevent="showNewspapers = true">
    </button-icon>

    <button-icon
      v-else
      role="button"
      tabindex="0"
      @click.prevent="showNewspapers = true">
      {{ $t('Consider for newspaper') }}
    </button-icon>

    <backlog-add--dropdown
      v-if="showNewspapers"
      v-on-clickaway="() => showNewspapers = false">
      <header>{{ $t('For which newspaper?') }}</header>

      <section>
        <ul>
          <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in containedIn}">
            <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
          </li>
        </ul>
      </section>
    </backlog-add--dropdown>
  </backlog-add-view>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex'
import { directive as onClickaway } from '@/lib/vue-clickaway'



export default {
  name: 'ConsiderPost',
  props: {
    post: Object,
    showText: Boolean
  },

  directives: {
    onClickaway
  },

  data() {
    return {
      showNewspapers: false,
//      backlog: {} // TODO provide initial state
    }
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

backlog-add-view
  position: relative

  button-icon
    border-radius: 100%
    display: inline-block
    height: $baseline * 1.25
    margin-left: $baseline / 4
    width: $baseline * 1.25

    background: #eee
    color: #555

    line-height: $baseline * 1.25
    text-align: center

    transition: 0.15s background

    &::before
      content: fa-content($fa-var-newspaper)

    &:focus,
    &:hover
      background: #ddd

backlog-add--dropdown
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
