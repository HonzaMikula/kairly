<template>
  <div class="empty-column-placeholder-view">
    <h2>{{ $t('Available actions') }}</h2>
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

  h2
    padding: $baseline 0

    font-weight: 600
    text-align: center

  nav
    display: flex
    align-items: stretch
    flex-wrap: wrap
    justify-content: center
    padding: 0 $baseline $baseline $baseline

  button
    background: transparent
    border: 0
    border-radius: 3px
    padding: $baseline / 4
    margin: 0 $baseline/4 $baseline/2 $baseline/4
    width: $baseline * 4

    background: #f5f5f5
    box-shadow: 2px 2px 4px #ddd, -2px -2px 4px #fff
    color: #555

    cursor: pointer

    @media (max-width: $mobile)
      width: $baseline * 4

    &:hover,
    &:focus
      color: #000
      background: #eee

    &.is-active
      background:#fff
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
