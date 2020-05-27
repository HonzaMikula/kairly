<template>
  <div v-on-clickaway="closeDialog" class="consider-post-view">
    <header>
      <h2>{{ $t('For which newspaper?') }}</h2>
      <strong
        v-b-tooltip
        class="consider-post--price"
        :title="$t('Article cost')"
      >
        <MoneyFormat :value="post.price" currency="Kč" />
      </strong>
    </header>

    <section v-if="step === 'step-1'" class="consider-post--step-1">
      <ul>
        <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in postBacklog}">
          <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
        </li>
      </ul>
    </section>

    <section v-else-if="step === 'step-2'" class="consider-post--step-2">
      <div class="consider-post--step-2--content">
        <h3>Upcoming issue</h3>
        <p>Will be release in ...</p>

        <label>
          <input v-model="acbd" name="position" type="radio"> To the top
        </label>

        <label v-for="section in upcomingIssueSections" :key="section.index">
          <input v-model="acbd" name="position" type="radio" :value="section.index"> {{ section.title }}
        </label>

        <label>
          <input v-model="acbd" name="position" type="radio"> To the bottom
        </label>

        <h3>Backlog</h3>
        <label>
          <input v-model="acbd" name="position" type="radio"> To the top
        </label>

        <label v-for="section in backlogSections" :key="section.index">
          <input v-model="acbd" name="position" type="radio" :value="section.index"> {{ section.title }}
        </label>

        <label>
          <input v-model="acbd" name="position" type="radio"> To the bottom
        </label>
      </div>

      <div class="consider-post--step-2--footer">
        <div>
          <button>Save</button>
        </div>

        <div>
          Save and add comment
        </div>
      </div>
    </section>

    <section v-else-if="step === 'add-comment'" class="consider-post--add-comment">
      add comments
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
    post: { type: Object, required: true }
  },

  data () {
    return {
      step: 0,
      selectedNewspaper: null
    }
  },

  computed: {
    ...mapState({
      backlog: state => state.backlog.userBacklog
    }),

    ...mapGetters(['userNewspapers']),

    postBacklog () {
      return this.backlog ? (this.backlog[this.post.id] || {}) : {}
    },

    backlogSections () {
      const posts = this.$store.state.backlog.newspaperBacklog[this.selectedNewspaper.fullName].considered.layout
      const sections = []
      posts.forEach((item, index) => {
        if (item.type === 'header') {
          sections.push({ title: item.title, index })
        }
      })
      return sections
    },

    upcomingIssueSections () {
      const posts = this.$store.state.backlog.newspaperBacklog[this.selectedNewspaper.fullName].upcoming.layout
      const sections = []
      posts.forEach((item, index) => {
        if (item.type === 'header') {
          sections.push({ title: item.title, index })
        }
      })
      return sections
    },
  },

  created () {
    if (this.userNewspapers.length > 1) {
      this.step = 'step-1'
    } else {
      this.step = 'step-2'
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
        this.step = 'step-2'
        this.selectedNewspaper = newspaper
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

    h2
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

//- Step 2
.consider-post--step-2
  padding: $baseline / 2

.consider-post--step-2--content

  h3
    font-weight: 600

  h3 + p
    margin-bottom: $baseline / 2

  label
    display: block
    margin-bottom: $baseline / 4

.consider-post--step-2--footer

  button
    width: 100%

// TODO
// Step 2
// - when it will be released
// - save it

// Step - Add comment
// - step add comment - style it up
// - save comment
// - save only when you have one newspaper

// Other
// - mobile version -> modal
// - maybe use vue bootstrap popover
// - translations
</style>
