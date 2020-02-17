<template>
  <div class="editorial-post--editorial crossroad">
    <h2>{{ $t('Editorials') }}</h2>
    <button
      @click="$emit('select', 'tweets')"
    >
      {{ $t('Select tweets') }}
    </button>
    <p>{{ $t('or') }}</p>
    <button
      @click="$emit('select', 'article')"
    >
      {{ $t('Write editorial') }}
    </button>
  </div>
</template>

<script>


export default {
  name: 'EditorialCrossroad',
}
</script>
<style lang="sass">
@import './styles/components/buttons'

//- Editorial Crossroad
.editorial-post--editorial.crossroad
  text-align: center

  h2
    margin-bottom: $baseline

    font-size: $fs-1
    font-weight: 600

  p
    margin: $baseline/2 0

  button
    +button(secondary, small)

</style>
