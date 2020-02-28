<template>
  <div 
    class="newspaper-backlog-post-toolbar-view"
    :class="{'is-shown': show}"
    >
    <nav>
      <!-- <button class="posts">{{ $t('Post') }}</button> -->

      <button
        class="comment"
        @click.prevent="addComment"
      >
        {{ $t('Comment') }}
      </button>

      <button
        class="heading"
        @click.prevent="addHeader"
      >
        {{ $t('Heading') }}
      </button>

      <button
        class="divider"
        @click.prevent="addHR"
      >
        {{ $t('Divider') }}
      </button>

      <button
        class="external-article"
        @click.prevent="addExternalLink"
      >
        {{ $t('External article') }}
      </button>

      <button 
        class="layout"
        :id="`layout-${backlog.name}-${index}`"
      >
        {{ $t('Special layout') }}
      </button>

      <b-popover
        :target="`layout-${backlog.name}-${index}`"
        placement="bottom"
        triggers="click blur"
        @click.stop
      >
        <ul>
          <li tabindex="0" @click="makeBox('cols-2-1', ['', 'editorial'])">
            <h6>{{ $t('Layout 2-1') }}</h6>
            <p>{{ $t('One main article, one smaller column') }}</p>
          </li>

          <li tabindex="1" @click="makeBox('cols-1-1', ['', ''])">
            <h6>{{ $t('Layout 1-1') }}</h6>
            <p>{{ $t('Two equal sections') }}</p>
          </li>

          <li tabindex="2" @click="makeBox('cols-1-1-1', ['', '', ''])">
            <h6>{{ $t('Layout 1-1-1') }}</h6>
            <p>{{ $t('Three equal sections') }}</p>
          </li>
        </ul>
      </b-popover>
    </nav>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import ErrorHandler from '@/mixins/ErrorHandler'
import { BPopover } from "bootstrap-vue";

export default {
  name: "NewspaperBacklogPostToolbar",

  components: {
    BPopover,
  },

  props: {
    index: Number,
    newspaper: Object,
    backlog: Object,
    show: Boolean
  },

  mixins: [ErrorHandler],

  methods: {
    ...mapActions({
      addLinkToBacklog: 'backlog/addLink'
    }),

    setBacklogItem(item) {
      this.$store.commit("backlog/setBacklogItem", {
        newspaper: this.newspaper,
        source: this.backlog.name,
        index: this.index,
        item
      });
    },

    makeBox(layout, columnsStyle) {
      this.setBacklogItem({
        //id: this.post.id, // keep same id to keep same NewspaperBacklogBox, NOT GOOD idea as long as post can be removed
        id: Math.random()
          .toString(36)
          .substring(2),
        type: "box",
        css: layout,
        columns: columnsStyle.map((css, idx) => {
          return {
            css,
            posts: []
          };
        })
      });
      this.$store.dispatch("backlog/save", { newspaper: this.newspaper });
    },

    async addExternalLink() {
      let url = window.prompt("URL")
      if (url === null) {
        return
      }

      try {
        await this.addLinkToBacklog({
          newspaper: this.newspaper,
          target: this.backlog.name,
          index: this.index,
          url
        })
      } catch (err) {
        this.handleError(err)
      }
    },

    async addComment() {
      const data = {
        type: 'comment',
        title: '',
        content: ''
      }
      const { post } = await this.$axios.$post(`/drafts`, data)
      const newspaper = this.newspaper

      this.$store.commit('backlog/registerPost', { newspaper, post })
      this.$store.commit('backlog/splice', {
        newspaper: newspaper,
        target: this.backlog.name,
        items: [{id: post.id, type: 'post'}],
        index: this.index,
        deleteCount: 0
      })
      this.$store.dispatch('backlog/save', { newspaper })
    },

    addHeader() {
      let title = window.prompt("Title")
      if (title === null) {
        return
      }
      title = title.trim()
      this.addHeaderItem(title === '' ? null : title)
    },

    addHR() {
      this.addHeaderItem(null)
    },

    addHeaderItem(title) {
      const newspaper = this.newspaper
      const item = {
        id: Math.random().toString(36).substring(2),
        type: 'header',
        title: title
      }
      this.$store.commit('backlog/splice', {
        newspaper: newspaper,
        target: this.backlog.name,
        items: [item],
        index: this.index,
        deleteCount: 0
      })
      this.$store.dispatch('backlog/save', { newspaper })
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.newspaper-backlog-post-toolbar-view
  height: $baseline / 2

  cursor: pointer

  transition: 0.3s all

  &:hover,
  &.is-shown
    height: $baseline * 2.5
    padding: $baseline/2 0
    transition: all 0.3s 0.3s

    nav
      background: #fff
      opacity: 1

      transition: opacity 0.3s 0.3s

  nav
    display: flex
    align-items: center
    justify-content: center
    padding: $baseline/2 $baseline

    opacity: 0

  button
    background: transparent
    border: 0
    padding: 0
    margin: 0 $baseline/2

    color: #777

    cursor: pointer

    &:hover,
    &:focus
      color: #000

    &::before
      +fa-icon()
      @extend .fas

      display: block
      margin-bottom: $baseline / 4

    &.posts::before
      content: fa-content($fa-var-newspaper)

    &.comment::before
      content: fa-content($fa-var-comment)

    &.heading::before
      content: fa-content($fa-var-heading)

    &.divider::before
      content: fa-content($fa-var-grip-lines)

    &.external-article::before
      content: fa-content($fa-var-external-link-alt)

    &.layout::before
      content: fa-content($fa-var-columns)

</style>
