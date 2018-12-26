<template>
  <modal-window @click="closeModal">
    <slot></slot>
  </modal-window>
</template>

<script>

export default {
  name: 'DialogWindowComponent',

  props: {
    closeModal: Function
  }
}
</script>

<style lang="sass">
modal-window
  position: fixed
  top: 0
  left: 0
  z-index: 100000000

  box-sizing: border-box
  display: flex
  padding: 0 $baseline/4
  align-items: center
  justify-content: center
  height: 100%
  width: 100%

  +blur(7px)

  @supports not (backdrop-filter: blur(10px))
    background: rgba(0, 0, 0, 0.3)

//- Dialog Window
modal-dialog
  position: relative
  z-index: 99999999999

  display: grid
  grid-template-rows: $baseline*2 1fr auto
  border-radius: $baseline / 2
  max-height: 90vh
  overflow: hidden

  background: #fff
  +box-shadow

  //- Header
  > header
    display: grid
    grid-template-columns: 1fr auto

    height: $baseline * 2

    background: $c-base
    color: #fff

    font-weight: 600
    line-height: $baseline * 2

    //- Dialog title
    h1
      padding: 0 $baseline

    //- Close button
    button-close
      height: $baseline * 2
      width: $baseline * 2

      opacity: 0.5

      cursor: pointer
      text-align: center

      transition: 0.15s opacity

      &:focus,
      &:hover
        opacity: 1


      &::before
        +fa-icon()
        @extend .fas

        content: fa-content($fa-var-times)

  //- Footer
  > footer
    padding: $baseline/2 $baseline

    background: #eee

    text-align: center

    //- action button
    button
      +subscribe-button

      border-radius: $baseline * 1.25/2
      height: $baseline * 1.25

      background: $c-base
      color: #fff

      line-height: $baseline * 1.25

      &:focus,
      &:hover
        background: darken($c-base, 10%)


</style>
