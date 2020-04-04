<template>
  <div class="info-message-view" :class="type">
    <slot />
  </div>
</template>

<script>

export default {
  name: 'InfoMessage',

  props: {
    type: { type: String, required: true }
  }
}
</script>

<style lang="sass">
.info-message-view
  position: fixed
  left: 50%
  bottom: $baseline
  z-index: 9999999999

  display: table
  border-radius: $baseline / 4
  padding: $baseline/4 $baseline/2
  transform: translateX(-50%)

  backdrop-filter: blur(10px) saturate(125%)

  &.success
    background: rgba($c-base, 0.5)

  &.error
    background: rgba($c-red, 0.5)

</style>
