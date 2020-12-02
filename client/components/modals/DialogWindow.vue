<template>
  <portal to="modal">
    <div
      class="modal-window"
      @click="onBackgroundClick"
    >
      <div
        class="modal-dialog"
        :class="customClass"
        role="dialog"
        @click.stop
      >
        <header>
          <slot name="header" />
          <div
            class="button-close"
            tabindex="0"
            role="button"
            @click="close"
          />
        </header>

        <main>
          <slot />
        </main>

        <footer v-if="!!this.$slots['footer']">
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </portal>
</template>

<script>

export default {
  name: 'DialogWindow',

  props: {
    customClass: { type: String, required: true },
    ignoreBackgroundClick: Boolean
  },

  beforeMount () {
    window.addEventListener('keyup', this.onKeyUp)
  },

  beforeDestroy () {
    window.removeEventListener('keyup', this.onKeyUp)
  },

  methods: {
    close () {
      this.$emit('close')
    },

    onBackgroundClick (event) {
      if (!this.ignoreBackgroundClick) {
        this.close()
      }
    },

    onKeyUp (event) {
      if (event.which === 27) {
        this.close()
      }
    },
  },
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'
@import './styles/components/mixins'

.modal-window
  position: fixed
  top: 0
  left: 0
  z-index: 1000

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

  @media (max-width: $mobile)
    align-items: flex-end
    padding: 0

//- Dialog Window
.modal-dialog
  position: relative
  z-index: 99999999999

  display: grid
  grid-template-rows: $baseline*2 1fr auto
  border-radius: $baseline / 2
  max-height: 90vh
  overflow: hidden

  background: #fff
  +box-shadow

  @media (max-width: $mobile)
    border-radius: $baseline/2 $baseline/2 0 0
    max-height: 60vh
    width: 100%
    max-width: 100%

  //- Header
  > header
    display: grid
    grid-template-columns: $baseline*2 1fr $baseline*2

    height: $baseline * 2

    background: #eee
    color: #000

    font-weight: 600
    line-height: $baseline * 2

    //- Dialog title
    > h1,
    > div
      text-align: center
      grid-column: 2 / span 1

    //- Back buton
    .back
      grid-column: 1 / span 1

      height: $baseline * 2
      width: $baseline * 2

      border: 0
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

        content: fa-content($fa-var-arrow-left)

    //- Close button
    .button-close
      grid-column: 3 / span 1

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

  //- Main
  > main
    overflow: auto

  //- Footer
  > footer
    padding: $baseline/2

    background: #eee

    text-align: center

    //- action button
    > button
      +button(primary, medium)

</style>
