<template>
  <backlog-add-view v-if="managedEditions.length">

    <button-icon
      role="button"
      tabindex="0"
      aria-label="Consider for Edition"
      v-tooltip.top="'Consider for Edition'"
      @click.prevent="showEditions = true">
    </button-icon>

    <backlog-add--dropdown
      v-if="showEditions"
      v-on-clickaway="() => showEditions = false">
      <header>For which edition?</header>

      <section>
        <ul>
          <li v-for="ed in managedEditions" :key="ed.id" :class="{'is-selected': ed.fullName in containedIn}">
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
  name: 'BacklogAdd',
  props: {
    post: Object
  },

  directives: {
    onClickaway
  },

  data() {
    return {
      showEditions: false,
//      backlog: {} // TODO provide initial state
    }
  },

  computed: {
    ...mapGetters(['managedEditions', 'backlog']),

    containedIn() {
      return this.backlog[this.post.id] || {}
    }
  },

  methods: {
    toggle(edition, ev) {
      if (edition.fullName in this.containedIn) {
        this.removeFromBacklog({edition, post: this.post})
      } else {
        this.addToBacklog({edition, post: this.post})
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
