<template>
  <modal-window @click="onClose">
    <slot></slot>
  </modal-window>
</template>

<script>

export default {
  name: 'DialogWindowComponent',

  props: {
    onClose: Function
  }
}
</script>

<style lang="sass">
modal-window
  position: fixed
  top: 0
  left: 0

  display: flex
  align-items: center
  justify-content: center
  height: 100%
  width: 100%

  background: rgba(0, 0, 0, 0.1)
  backdrop-filter: blur(5px)

//- Dialog Window
modal-dialog
  position: relative

  display: grid
  grid-template-rows: $baseline*2 1fr $baseline*2
  border-radius: $baseline / 2
  min-height: 500px
  max-height: 95vh
  overflow: hidden
  width: 970px

  background: #fff

  //- Header
  > header
    height: $baseline * 2
    padding: 0 $baseline

    background: $c-base
    color: #fff

    font-weight: 600
    line-height: $baseline * 2

  //- Footer
  > footer
    padding: $baseline/4 $baseline

    background: #eee

    text-align: center

    //- action button
    button
      +subscribe-button

      height: $baseline * 1.25

      background: $c-base
      color: #fff

      &:focus,
      &:hover
        background: darken($c-base, 10%)


</style>
