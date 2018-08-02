<template>
  <backlog-add-view v-if="managedNewspapers.length">

    <button-icon
      v-if="!showText"
      role="button"
      tabindex="0"
      aria-label="Consider for newspaper"
      v-tooltip.top="'Consider for newspaper'"
      @click.prevent="showNewspapers = true">
    </button-icon>

    <button-icon
      v-else
      role="button"
      tabindex="0"
      @click.prevent="showNewspapers = true">
      Consider for newspaper
    </button-icon>

    <backlog-add--dropdown
      v-if="showNewspapers"
      v-on-clickaway="() => showNewspapers = false">
      <header>For which newspaper?</header>

      <section>
        <ul>
          <li v-for="ed in managedNewspapers" :key="ed.id" :class="{'is-selected': ed.fullName in containedIn}">
            <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
          </li>
        </ul>
      </section>
    </backlog-add--dropdown>
  </backlog-add-view>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import * as api from '@/api'

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
    ...mapGetters(['managedNewspapers', 'backlog']),

    containedIn() {
      return this.backlog[this.post.id] || {}
    }
  },

  methods: {
    toggle(newspaper, ev) {
      if (newspaper.fullName in this.containedIn) {
        this.removeFromBacklog({newspaper, post: this.post})
      } else {
        this.addToBacklog({newspaper, post: this.post})
      }
      ev.target.blur()
    },

    ...mapActions(['addToBacklog', 'removeFromBacklog'])
  }
}
</script>

<style lang="sass">
backlog-add-view
  position: relative

  button-icon
    &::before
      content: $fa-var-newspaper-o

backlog-add--dropdown
  +context-menu

  position: absolute
  left: 50%

  top: 40px
  z-index: 1

  @media (max-width: 1120px)
    left: inherit
    right: -$baseline/4

    &::after
      left: inherit
      right: 5px

  li
    a::after
      content: $fa-var-check

    &.is-selected a::after
      opacity: 1 !important

</style>
