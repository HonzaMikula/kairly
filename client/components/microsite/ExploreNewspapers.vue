<template>
  <section class="microsite-explore">
    <h2>{{ $t('We believe in human editors.') }} <br> {{ $t('Read recently published newspapers.') }}</h2>

    <div class="microsite-explore--crossroad">
      <div v-for="category in exploreNewspapers" :key="category.name">
        <h3>{{category.name}}</h3>
        <ul>
          <li v-for="item in category.newspapers" :key="item.id" :class="{'is-selected': item.id == selectedNewspaper}">
            <a :href="item.id" @click.prevent="showNewspaper(item.id)">{{ item.name }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div class="microsite-explore--issue" :class="{'is-expanded': expandNewspaper}">
      <IssueWrapper v-if="issue" :issue="issue" showTail></IssueWrapper>

      <p>{{ $t('That\'s it. You read the whole issue.') }}</p>

      <button v-if="!expandNewspaper" @click="showMore()">{{ $t('Show more') }}</button>  
    </div>
  </section>
</template>

<script>
import NEWSPAPERS from '@/topNewspapers'
import IssueWrapper from '@/components/IssueWrapper'


export default {
  name: 'ExploreNewspapers',

  components: {
    IssueWrapper
  },

  data() {
    return {
      newspapers: null,
      issue: null,
      expandNewspaper: false,
      exploreNewspapers: NEWSPAPERS,
      selectedNewspaper: 'janmikula/malostranskenoviny'
    }
  },

  methods: {
    async showNewspaper(newspaperId) {
      this.selectedNewspaper = newspaperId

      this.$ga.event({
        eventCategory: 'Homepage',
        eventAction: 'Show newspaper',
        eventLabel: newspaperId
      })

      const { newspaper, issue, links } = await this.$store.dispatch('getNewspaperDetail', {
        newspaperId: newspaperId
      })
      this.issue = issue
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

    this.issue = issue
  }

}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'


.microsite-explore
  padding-bottom: $baseline * 2

  @media (max-width: $mobile)
    padding: $baseline/2 $baseline/2

  > h2
    margin-bottom: $baseline / 2

    font-size: $fs-4
    font-weight: 900
    line-height: 1.42

    @media (max-width: $mobile)
      font-size: $fs-3
      line-height: $baseline * 1.2

.microsite-explore--crossroad
  display: flex
  padding: $baseline $baseline*2
  margin: 0 (-$baseline*2)

  background: #fafafa
  border-bottom: 1px solid #eee

  @media (max-width: $mobile)
    margin: 0 (-$baseline/2)
    padding: $baseline/2
    overflow-x: auto
    -webkit-overflow-scrolling: touch

  > div
    flex: 1
    margin-right: $baseline / 2

    &:last-of-type
      margin-right: 0

    @media (max-width: $mobile)
      min-width: 200px
      

  h3
    margin-bottom: $baseline / 2

    font-size: $fs-2
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

.microsite-explore--issue
  position: relative
  max-height: 700px
  overflow: hidden
  margin: 0 (-$baseline*2)
  padding: 0 $baseline * 2

  background: #fafafa

  @media (max-width: $mobile)
    margin: 0 (-$baseline/2)
    padding: 0

  timeline-newspaper
    margin-top: $baseline

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
    
</style>
