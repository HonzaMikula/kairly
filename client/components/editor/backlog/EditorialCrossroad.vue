<template>
  <div class="editorial-post--editorial crossroad">
    <h2>Editorials</h2>
    <button
      @click="$emit('select', 'tweets')"
    >
      Select tweets
    </button>
    <p>or</p>
    <button
      @click="$emit('select', 'article')"
    >
      Write editorial
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
