<template>
  <DialogWindow
    v-if="active"
    custom-class="consider-post-dialog"
    ignore-background-click
    @close="closeModal"
  >
    <template #header>
      <template v-if="step === 'step-1'">
        <h1>{{ $t('For which newsletter?') }}</h1>
      </template>

      <template v-else-if="step === 'step-2'">
        <button class="back" @click="goBack()" />
        <h1>{{ selectedNewspaper.title }}</h1>
      </template>
    </template>

    <div class="consider-post-view">
      <section
        v-if="step === 'step-1'"
        class="consider-post--step-1"
        :class="{'two-columns': userNewspapers.length > 5}"
      >
        <ul>
          <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in postBacklog}">
            <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
          </li>
        </ul>
      </section>

      <section v-else-if="step === 'step-2'" class="consider-post--step-2">
        <div class="consider-post--step-2--content">
          <section>
            <h3>{{ $t('Backlog') }}</h3>
            <p>{{ $t('Post that are considered.') }}</p>

            <div class="consider-post--step2--sections">
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['considered', 0]"
                >
                {{ $t('To the top') }}
              </label>
            </div>

            <div
              v-for="section in backlogSections"
              :key="section.index"
              class="consider-post--step2--sections"
            >
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['considered', section.index + 1]"
                >
                {{ section.title }}
              </label>
            </div>

            <div class="consider-post--step2--sections">
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['considered', -1]"
                >
                {{ $t('To the bottom') }}
              </label>
            </div>
            <button
              class="consider-post--step2--add-section"
              @click="addHeading('considered')"
            >
              {{ $t('Add section') }}
            </button>
          </section>

          <section>
            <h3>{{ $t('Upcoming issue') }}</h3>
            <p>{{ $t('Will be released') }} {{ nextRelease }}.</p>

            <div class="consider-post--step2--sections">
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['upcoming', 0]"
                >
                {{ $t('To the top') }}
              </label>
            </div>

            <div
              v-for="section in upcomingIssueSections"
              :key="section.index"
              class="consider-post--step2--sections"
            >
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['upcoming', section.index + 1]"
                >
                {{ section.title }}
              </label>
            </div>

            <div class="consider-post--step2--sections">
              <label>
                <input
                  v-model="position"
                  name="position"
                  type="radio"
                  :value="['upcoming', -1]"
                >
                {{ $t('To the bottom') }}
              </label>
            </div>
            <button
              class="consider-post--step2--add-section"
              @click="addHeading('upcoming')"
            >
              {{ $t('Add section') }}
            </button>
          </section>
        </div>
      </section>
    </div>
    <template v-if="step === 'step-2'" #footer>
      <button @click="save()">{{ $t('Save') }}</button>
    </template>
  </DialogWindow>
</template>

<script>
import moment from 'moment'
import { mapGetters, mapState, mapActions } from 'vuex'

import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'ConsiderPost',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin],

  props: {
    post: { type: Object, required: true }
  },

  data () {
    return {
      position: [],
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

    nextRelease () {
      return moment(this.$store.getters['entities/getNewspaper'](this.selectedNewspaper.fullName).nextRelease).from()
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
    addHeading (target) {
      let title = window.prompt('Title')
      if (title === null) {
        return
      }
      title = title.trim()
      const newspaper = this.selectedNewspaper
      const item = {
        id: Math.random().toString(36).substring(2),
        type: 'header',
        title
      }
      this.$store.commit('backlog/splice', {
        newspaper,
        target,
        items: [item],
        index: -1,
        deleteCount: 0
      })
      this.$store.dispatch('backlog/save', { newspaper })
    },

    goBack () {
      this.step = 'step-1'
      this.selectedNewspaper = null
    },

    async toggle (newspaper, ev) {
      const backlogName = this.postBacklog[newspaper.fullName]
      if (backlogName) {
        this.removeFromBacklog({
          newspaper,
          source: backlogName,
          post: this.post
        })
      } else {
        await this.loadNewspaperBacklog(newspaper.fullName)
        this.step = 'step-2'
        this.selectedNewspaper = newspaper
      }

      document.activeElement.blur()
    },

    save () {
      const newspaper = this.selectedNewspaper
      const target = this.position[0]
      const index = this.position[1]

      this.addToBacklog({
        newspaper,
        target,
        post: this.post,
        index
      })

      this.closeModal()
      this.step = 'step-1'
      this.selectedNewspaper = null
    },

    ...mapActions({
      addToBacklog: 'backlog/add',
      removeFromBacklog: 'backlog/remove',
      loadNewspaperBacklog: 'backlog/loadNewspaperBacklog',
    })
  }
}
</script>

<style lang="sass">
@import './styles/components/context-menu'
@import './styles/components/buttons'

.consider-post-dialog
  width: 480px

  @media (max-width: $mobile)
    max-width: 100%

.consider-post--step-1
  padding: $baseline / 2

  &.two-columns
    columns: 2

    @media (max-width: $mobile)
      columns: 1

  li
    a
      color: #000

      &::before
        opacity: 0.5

      &:hover::before,
      &:focus::before
        opacity: 1

    a::before
      display: inline-block
      height: 10px
      width: 10px

      background: #555
      border-radius: 100%

      margin-right: $baseline / 2

      content: ''

    &.is-selected
      a
        font-weight: 600
      a::before
        background: $c-base
        opacity: 1

//- Step 2
.consider-post--step-2
  padding: $baseline / 2

.consider-post--step-2--content
  display: grid
  grid-template-columns: 1fr 1fr
  grid-column-gap: $baseline

  h3
    font-weight: 600

  h3 + p
    margin-bottom: $baseline / 4

    font-size: $fs--1
    line-height: 1.42

    color: #555

  label
    display: block
    margin-bottom: $baseline / 4

    white-space: nowrap
    text-overflow: ellipsis
    overflow: hidden

  > section:first-of-type
    margin-bottom: $baseline / 2

.consider-post--step2--sections
  display: flex

  > label
    flex: 1

.consider-post--step2--add-section
  padding: 0

  background: transparent
  border: 0
  color: $c-base

  line-height: $baseline
  font-family: $ff-sans
  font-size: $fs-0

  &::before
    +fa-icon()
    @extend .fas

    margin: 0 $baseline / 4

    content: fa-content($fa-var-plus)

.consider-post--step-2--footer

  button
    +button(primary, small)

    width: 100%

</style>
