<template>
  <div class="empty-column-placeholder-view">
    <h2>{{ $t('Available actions') }}</h2>
    <nav>
      <slot/>
    </nav>
  </div>
</template>

<script>
export default {
  name: "EmptyColumnPlaceholder"
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.empty-column-placeholder-view

  h2
    padding: $baseline 0

    font-weight: 600
    text-align: center

  nav
    display: flex
    align-items: center
    justify-content: center
    padding: 0 $baseline $baseline $baseline

  button
    background: transparent
    border: 0
    padding: 0
    margin: 0 $baseline/2

    color: #777

    cursor: pointer

    &:hover,
    &:focus
      color: #000

    &::before
      +fa-icon()
      @extend .fas

      display: block
      margin-bottom: $baseline / 4

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
