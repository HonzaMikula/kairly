<template>
  <div class="newspaper-backlog-post-toolbar-view">
    <nav>
      <button class="posts">{{ $t('Post') }}</button>

      <button class="comment">{{ $t('Comment') }}</button>

      <button class="heading">{{ $t('Heading') }}</button>

      <button class="divider">{{ $t('Divider') }}</button>

      <button class="external-article">{{ $t('External article') }}</button>

      <button class="layout">{{ $t('Special layout') }}</button>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NewspaperBacklogPostToolbar"
}
</script>

<style lang="sass">
@import './styles/components/buttons'

.newspaper-backlog-post-toolbar-view

  height: $baseline / 2

  cursor: pointer

  transition: 0.3s all

  &:hover
    height: $baseline * 2.5
    padding: $baseline/2 0
    transition: all 0.3s 0.3s

    nav
      background: #fff
      opacity: 1

      transition: opacity 0.3s 0.3s

  nav
    display: flex
    align-items: center
    justify-content: center
    padding: $baseline/2 $baseline

    opacity: 0

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

    &.posts::before
      content: fa-content($fa-var-newspaper)

    &.comment::before
      content: fa-content($fa-var-comment)

    &.heading::before
      content: fa-content($fa-var-heading)

    &.divider::before
      content: fa-content($fa-var-grip-lines)

    &.external-article::before
      content: fa-content($fa-var-external-link-alt)

    &.layout::before
      content: fa-content($fa-var-columns)

</style>
