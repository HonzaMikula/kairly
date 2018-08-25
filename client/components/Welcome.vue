<template>
  <timeline-welcome>

    <welcome-view>
      <h1>Welcome to Kairly!</h1>

      <welcome--roles>
        <div>
          <h3>Authors</h3>
          <p>
            Authors focus on writing.
            They are creating high quality articles &amp; tweets.
          </p>
        </div>

        <div>
          <h3>Editors</h3>
          <p>
            Editors run their newspaper.
            They are selecting the best articles &amp; tweets from authors.
          </p>
        </div>

        <div>
          <h3>Readers</h3>
          <p>
            Readers choose what they want to read and when.
            They subscribe either directly to authors or to newspapers.
          </p>
        </div>
      </welcome--roles>

      <nuxt-link to="/explore">Start exploring authors &amp; newspapers</nuxt-link>
    </welcome-view>


    <template v-if="!loading">
      <Issue :issue="issue" :subscription="newspaper.subscription" />

      <nuxt-link to="/explore">Start exploring</nuxt-link>
    </template>
  </timeline-welcome>
</template>

<script>
import { mapActions } from 'vuex'

import Issue from '@/components/IssueWrapper'

export default {
  name: 'Welcome',

  components: {
    Issue
  },

  data() {
    return {
      loading: true,
      newspaper: null,
      issue: null,
    }
  },

  methods: mapActions(['getNewspaperDetail']),

  async created() {
    const resp = await getNewspaperDetail({
      newspaperId: 'janmikula/kairly',
      issue: 1
    })
    this.newspaper = resp.newspaper
    this.issue = resp.issue
    this.loading = false
  }
}
</script>

<style lang="sass">
//- Welcome Newspaper
timeline-welcome
  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5


//- Welcome box
welcome-view
  display: block
  padding: $baseline
  margin-bottom: $baseline * 2

  background: #eee
  border: 1px dashed #ccc

  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center

  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

//- Roles
welcome--roles
  display: flex
  max-width: 900px
  margin: 0 auto

  font-family: $ff-serif

  div
    position: relative

    flex: 1
    padding: $baseline 0
    margin-right: $baseline*2

    &::after
      +fa-icon()

      position: absolute
      right: -$baseline * 1.25
      top: $baseline * 3

      content: $fa-var-arrow-right

    &:last-of-type
      margin-right: 0

      &::after
        display: none

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-2
    font-weight: 600

</style>
