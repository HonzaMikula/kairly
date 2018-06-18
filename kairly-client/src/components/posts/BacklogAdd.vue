<template>
  <backlog-add-view v-if="managedEditions">
    
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

      <ul>
        <li v-for="ed in managedEditions" :key="ed.id" :class="{'is-selected': backlog[ed.id]}">
          <a href="#" @click.prevent="add(ed)">{{ ed.title }}</a>
        </li>
      </ul>
      
    </backlog-add--dropdown>
  </backlog-add-view>
</template>

<script>
import { mapState } from 'vuex'
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
      backlog: {} // TODO provide initial state
    }
  },

  computed: mapState({
    managedEditions: state => state.managedEditions
  }),

  methods: {
    add(edition) {
      api.addToBacklog(edition.id, this.post.id)
      .then(() => {
        this.backlog = {...this.backlog, [edition.id]: true}
      })
    }
  }
}
</script>

<style lang="sass">
backlog-add-view
  position: relative

  button-icon
    opacity: 0.5
    
    cursor: pointer

    transition: 0.15s opacity

    &:focus,
    &:hover
      opacity: 1

    &::before
      content: $fa-var-newspaper-o

backlog-add--dropdown
  position: absolute
  left: 50%
  top: 40px
  z-index: 1

  margin-left: -125px

  display: block
  border-radius: 5px
  width: 250px

  background: #fff
  border: 1px solid #eee
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.15)

  //- arrow up
  &::after
    bottom: 100%
    left: 50%
    border: solid transparent
    content: " "
    height: 0
    width: 0
    position: absolute
    pointer-events: none
    border-bottom-color: lighten($c-base, 30%)
    border-width: 15px
    margin-left: -15px


  //- header
  header
    position: relative

    border-radius: 5px 5px 0 0

    background: lighten($c-base, 30%)
    color: #000

    font-weight: 600
    font-size: $fs--1
    line-height: $baseline * 1.25
    text-align: center

  li
    font-size: $fs--1
    a
      position: relative

      display: block
      padding: 0 $baseline/2

      color: #000

      line-height: $baseline * 1.25
      text-decoration: none

      transition: 0.15s all

      &::after
        +fa-icon()

        position: absolute
        right: $baseline / 2
        top: 8px

        color: darken($c-base, 20%)
        opacity: 0

        font-size: $fs--2

        content: $fa-var-check

        transition: 0.15s all 

      &:hover,
      &:focus
        background: lighten($c-base, 40%)

        &::after
          opacity: 0.5

    &.is-selected a::after
      opacity: 1        
  
   


</style>
