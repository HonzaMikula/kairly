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
          <slot name="header"/>
          <div
            class="button-close"
            tabindex="0"
            role="button"
            @click="close"
          />
        </header>

        <main>
          <slot/>
        </main>

        <footer v-if="!!this.$slots['footer']">
          <slot name="footer"/>
        </footer>
      </div>
    </div>
  </portal>
</template>

<script>

export default {
  name: 'DialogWindow',

  props: {
    customClass: String,
    ignoreBackgroundClick: Boolean
  },

  methods: {
    close() {
      this.$emit('close')
    },

    onBackgroundClick(event) {
      if (!this.ignoreBackgroundClick) {
        this.close()
      }
    },

    onKeyUp(event) {
      if (event.which === 27) {
        this.close()
      }
    },
  },

  beforeMount() {
    window.addEventListener('keyup', this.onKeyUp);
  },

  beforeDestroy() {
    window.removeEventListener('keyup', this.onKeyUp)
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
      padding: 0 $baseline/2

    //- Close button
    .button-close
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
    button
      +button(primary, medium)

</style>
