<template>
  <DialogWindow
    v-if="active"
    custom-class="consider-post-dialog"
    ignore-background-click
    @close="closeModal"
  >
    <template #header>
      <template v-if="step === 'step-1'">
        <h2>{{ $t('For which newsletter?') }}</h2>
        <strong
          v-b-tooltip
          class="consider-post--price"
          :title="$t('Article cost')"
        >
          <MoneyFormat :value="post.price" currency="Kč" />
        </strong>
      </template>

      <template v-else-if="step === 'step-2'">
        <button class="back" @click="goBack()" />
        <h2>{{ selectedNewspaper.title }}</h2>
      </template>
    </template>

    <div v-on-clickaway="closeDialog" class="consider-post-view">
      <section v-if="step === 'step-1'" class="consider-post--step-1">
        <ul>
          <li v-for="ed in userNewspapers" :key="ed.fullName" :class="{'is-selected': ed.fullName in postBacklog}">
            <a href="#" @click.prevent="toggle(ed, $event)">{{ ed.title }}</a>
          </li>
        </ul>
      </section>

      <section v-else-if="step === 'step-2'" class="consider-post--step-2">
        <div class="consider-post--step-2--content">
          <h3>{{ $t('Upcoming issue') }}</h3>
          <p>{{ $t('Will be released') }} {{ nextRelease }}.</p>

          <label>
            <input
              v-model="position"
              name="position"
              type="radio"
              :value="['upcoming', 0]"
            >
            {{ $t('To the top') }}
          </label>

          <label v-for="section in upcomingIssueSections" :key="section.index">
            <input
              v-model="position"
              name="position"
              type="radio"
              :value="['upcoming', section.index + 1]"
            >
            {{ section.title }}
          </label>

          <label>
            <input
              v-model="position"
              name="position"
              type="radio"
              :value="['upcoming', -1]"
            >
            {{ $t('To the bottom') }}
          </label>

          <h3>{{ $t('Considered posts') }}</h3>
          <label>
            <input
              v-model="position"
              name="position"
              type="radio"
              :value="['considered', 0]"
            >
            {{ $t('To the top') }}
          </label>

          <label v-for="section in backlogSections" :key="section.index">
            <input
              v-model="position"
              name="position"
              type="radio"
              :value="['considered', section.index + 1]"
            >
            {{ section.title }}
          </label>

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
      </section>
    </div>
    <template #footer>
      <div>
        <button @click="save()">{{ $t('Save') }}</button>
      </div>
    </template>
  </DialogWindow>
</template>

<script>
import moment from 'moment'
import { mapGetters, mapState, mapActions } from 'vuex'
import { directive as onClickaway } from '@/lib/vue-clickaway'

import MoneyFormat from '@/components/widgets/MoneyFormat'
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'ConsiderPost',

  directives: {
    onClickaway
  },

  components: {
    MoneyFormat,
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
    closeDialog () {
      this.$emit('closeConsiderPostDialog')
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

      this.closeDialog()
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
  max-width: 640px

.consider-post-view
  //- header
  header
    display: flex
    padding: 0 $baseline/2

    h2
      margin-right: auto

    //- back button
    .back
      margin-left: (-$baseline/2)
      // margin-right: $baseline/4
      padding: 0 $baseline/2

      border: 0
      background: transparent

      cursor: pointer

      &:hover,
      &:focus
        background: lighten($c-base, 15%)

      &::before
        +fa-icon()
        @extend .fas

        content: fa-content($fa-var-arrow-left)

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
    font-size: $fs--1
    line-height: 1.42

    color: #555

  label
    display: block
    margin-bottom: $baseline / 4

.consider-post--step-2--footer

  button
    +button(primary, small)

    width: 100%

</style>
