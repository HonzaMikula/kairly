<template>
  <div class="empty-column-placeholder-view">
    <nav>
      <slot />
    </nav>
  </div>
</template>

<script>
export default {
  name: 'EmptyColumnPlaceholder'
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.empty-column-placeholder-view

  .is-empty &
    padding-top: $baseline

  nav
    display: flex
    align-items: stretch
    flex-wrap: wrap
    justify-content: center
    padding: 0 $baseline/2 $baseline/2 $baseline/2

  button
    margin: 0 $baseline/2
    padding: 0
    border: 0
    background: transparent

    cursor: pointer

    &:hover::before,
    &:focus::before
      color: #000
      background: #ddd

    &::before
      +fa-icon()
      @extend .fas

      display: block
      border-radius: 100%
      border: 1px solid #ddd
      height: $baseline * 1.5
      width: $baseline * 1.5
      line-height: $baseline * 1.5
      text-align: center

      background: #eee
      box-shadow: 2px 2px 4px #ddd, -2px -2px 4px #fff
      color: #000

    &.add-posts::before
      content: fa-content($fa-var-newspaper)

    &.toggle-editorial::before
      content: fa-content($fa-var-clipboard)

    &.add-comment::before
      content: fa-content($fa-var-comment)

    &.add-external::before
      content: fa-content($fa-var-external-link-alt)

.cols-1-1-1
  .empty-column-placeholder-view
    nav
      flex-wrap: wrap

      button
        margin-bottom: 10px
</style>
