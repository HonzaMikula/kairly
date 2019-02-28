<template>
  <section class="microsite-howitworks">
    <h2>{{ $t('How the platform works?') }}</h2>

    <picture>
      <img src="~assets/homepage/kairly-howitworks.jpg" />
    </picture>
  </section>
</template>

<script>
export default {
  name: 'HowItWorks'
}
</script>

<style lang="sass">
//- Mixin
=heading
  font-size: $fs-5
  font-weight: 900
  line-height: $baseline * 2

  @media (max-width: $mobile)
    font-size: $fs-3
    line-height: $baseline * 1.2

//- Image how it works
.microsite-howitworks
  margin-bottom: $baseline * 2

  @media (max-width: 950px)
    padding: $baseline $baseline 0 $baseline

  @media (max-width: $mobile)
    padding: $baseline $baseline/2
    margin-bottom: 0

  h2
    +heading

    margin-bottom: $baseline

  picture
    display: block
    margin: 0 (-$baseline*2)

    @media (max-width: 1050px)
      margin: 0

    @media (max-width: $mobile)
      margin: 0

  img
    width: 100%
</style>
