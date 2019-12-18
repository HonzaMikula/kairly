<template>
  <section class="explore-widget-view">
    <h2>
      <slot>
        {{ $t('We believe in human editors.') }}
        <br>
        {{ $t('Read recently published newsletters.') }}
      </slot>
    </h2>

    <div class="explore-widget--crossroad">
      <div v-for="category in exploreNewspapers" :key="category.name">
        <h3>{{category.name}}</h3>
        <ul>
          <li v-for="item in category.newspapers" :key="item.id" :class="{'is-selected': item.id == selectedNewspaper}">
            <a :href="item.id" @click.prevent="showNewspaper(item.id)">{{ item.name }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div
      v-if="issue"
      class="explore-widget--issue">
      <nav class="explore-widget--issue--navigation" v-if="links.prev || links.next">
        <button
          v-if="links.prev"
          v-b-tooltip
          :title="$t('Previous issue')"
          class="previous"
          @click="showNewspaper(selectedNewspaper, links.prev)"
        ></button>

        <button
          v-if="links.next"
          v-b-tooltip
          :title="$t('Next issue')"
          class="next"
          @click="showNewspaper(selectedNewspaper, links.next)"
        ></button>
      </nav>

      <IssueWrapper :issue="issue" showTail></IssueWrapper>

      <div class="explore-widget--issue--subscribe" v-if="loggedIn">
        <NewspaperSubscriptionButton :newspaper="newspaper" />
        <p>{{ periodicity }}</p>
      </div>

     </div>
  </section>
</template>

<script>
import NEWSPAPERS from '@/topNewspapers'
import { mapState } from 'vuex'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import IssueWrapper from '@/components/IssueWrapper'
import NewspaperSubscriptionButton from '@/components/widgets/NewspaperSubscriptionButton'

export default {
  name: 'ExploreNewspapers',

  components: {
    IssueWrapper,
    NewspaperSubscriptionButton
  },

  mixins: [PeriodicityMixin],

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    periodicity() {
      return this.getPeriodicityLabel(this.newspaper.periodicity)
    },
  },

  data() {
    return {
      newspaper: null,
      newspapers: null,
      issue: null,
      links: null,
      expandNewspaper: false,
      exploreNewspapers: NEWSPAPERS,
      selectedNewspaper: 'janmikula/malostranskenoviny'
    }
  },

  methods: {
    async showNewspaper(newspaperId, issueId) {
      this.selectedNewspaper = newspaperId

      if (issueId) {
        issueId = issueId.split('/').slice(-1)[0]
      }

      this.$ga.event({
        eventCategory: 'Homepage',
        eventAction: 'Show newspaper',
        eventLabel: newspaperId
      })

      const { newspaper, issue, links } = await this.$store.dispatch('getNewspaperDetail', {
        newspaperId: newspaperId,
        issue: issueId
      })
      this.newspaper = newspaper
      this.issue = issue
      this.links = links
    },

    showMore() {
      this.expandNewspaper = true

      this.$ga.event({
        eventCategory: 'Homepage',
        eventAction: 'Show more',
        eventLabel: this.selectedNewspaper
      })
    }
  },

  async created() {
    const { newspaper, issue, links } = await this.$store.dispatch('getNewspaperDetail', {
      newspaperId: 'janmikula/malostranskenoviny'
    })

    this.newspaper = newspaper
    this.issue = issue
    this.links = links
  }

}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'


.explore-widget-view
  display: grid
  grid-template-columns: 7fr 3fr
  grid-template-rows: auto
  padding-bottom: $baseline * 2

  @media (max-width: $mobile)
    grid-template-columns: 10fr

  > h2
    grid-column: 1 / span 2
    margin-bottom: $baseline / 2

    font-size: $fs-4
    font-weight: 900
    line-height: 1.42

    @media (max-width: $mobile)
      margin: $baseline / 2
      font-size: $fs-3
      line-height: $baseline * 1.2

.explore-widget--crossroad
  z-index: 1
  grid-column: 2
  grid-row: 2
  padding: $baseline $baseline

  @media (max-width: $mobile)
    display: none

  background: #fafafa
  border-bottom: 1px solid #eee

  @media (max-width: $mobile)
    margin: 0 (-$baseline/2)
    padding: $baseline/2
    overflow-x: auto
    -webkit-overflow-scrolling: touch

  > div
    flex: 1
    margin-bottom: $baseline / 2

    @media (max-width: $mobile)
      min-width: 200px


  h3
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      font-size: $fs-1

  li
    a
      color: $c-base

    &.is-selected
      font-weight: 600

      a
        color: #000

.explore-widget--issue
  position: relative

  grid-column: 1 / span 2
  grid-row: 2
  max-height: 700px
  overflow: hidden
  margin: 0 (-$baseline*2)
  padding: 0 $baseline * 2

  background: #fafafa

  @media (max-width: $mobile)
    margin: 0
    padding: 0

  timeline-newspaper
    margin-top: $baseline
    transform: scale(0.7)
    transform-origin: top left

    @media (max-width: $mobile)
      transform: none

  &.is-expanded
    max-height: none

    &::after
      display: none

  &::after
    position: absolute
    bottom: 0
    left: 0

    height: $baseline * 5
    width: 100%

    background: linear-gradient(to top, rgba(255, 255, 255, 1), transparent)

    content: ''

  //- Show more
  > button
    +button
    position: absolute
    left: 50%
    bottom: 0
    z-index: 1

    transform: translateX(-50%)

  //- That's it...
  > p
    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600
    line-height: 1.42
    text-align: center

    padding-bottom: $baseline

//- Navigation between issues
.explore-widget--issue--navigation
  display: grid
  grid-template-columns: min-content min-content
  grid-template-areas: "prev-link next-link"
  grid-column-gap: $baseline / 2
  padding-top: $baseline / 2
  margin-bottom: -($baseline * 2.375)

  @media (max-width: $mobile)
    grid-template-areas: "prev-link . next-link"
    grid-template-columns: min-content 1fr min-content

  button
    position: relative
    z-index: 3

    display: block
    border-radius: 100%
    height: $baseline * 1.5
    width: $baseline * 1.5

    background: #fff
    border: 0
    color: #000

    cursor: pointer
    line-height: $baseline * 1.5
    text-align: center

    &:hover,
    &:focus
      background: $c-base
      color: #fff

    &.is-disabled
      opacity: 0.5

      cursor: default
      pointer-events: none

      &:hover,
      &:focus
        background: #fff
        color: #000

    &::before
      +fa-icon()
      @extend .fas

    &.previous
      grid-area: prev-link

      &::before
        content: fa-content($fa-var-arrow-left)

    &.next
      grid-area: next-link

      &::before
        content: fa-content($fa-var-arrow-right)

//- Subscribe
.explore-widget--issue--subscribe
  position: absolute
  top: $baseline
  right: $baseline * 2

  text-align: center

  @media (max-width: $mobile)
    position: static
    margin: (-$baseline/2) 0 $baseline/2 0

  //- periodicity
  > p
    color: #555

    font-size: $fs--1

</style>
