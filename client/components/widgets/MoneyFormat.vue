<template>
  <span>
    {{ forceSign && numValue > 0 ? '+' : '' }}{{ formatted }} {{ currency ? currency : '' }}
  </span>
</template>

<script>
export default {
  name: 'MoneyFormat',

  props: {
    value: [Number, String],
    currency: String,
    short: { type: Boolean, default: false },
    forceSign: { type: Boolean, default: false }
  },

  computed: {
    numValue () {
      if (typeof this.value.toFixed === 'function') {
        return this.value
      }
      return parseFloat(this.value)
    },

    formatted () {
      let { value } = this
      if (value === null) {
        return ''
      }
      if (typeof value.toFixed === 'function') {
        value = value.toFixed(2)
      }
      if (this.short) {
        const parts = value.split('.')
        if (parseInt(parts[1]) === 0) {
          value = parts[0]
        }
      }
      return value
    }
  }
}
</script>

<style lang="sass">
</style>
