<template>
  <footer class="microsite-footer">
    <div>
      <h2 itemprop="name"><nuxt-link to="/">Kairly</nuxt-link></h2>

      <p>
        {{ $t('Stop be distracted.') }}
        <br>
        {{ $t('Grow healthy reading habits.') }}
      </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style lang="sass">
//- Footer
.microsite-footer
  position: relative

  display: flex
  align-items: center
  justify-content: center
  height: 400px
  max-width: none !important

  background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover

  color: #fff

  font-family: $ff-serif
  text-align: center

  h2
    display: table
    padding: 0 $baseline/2
    margin: 0 auto
    margin-bottom: $baseline

    background: #fff
    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: left

    @media (max-width: $mobile)
      font-size: $fs-3
      line-height: $baseline * 1.5

    a
      color: #000

  p
    display: table
    padding: 0 $baseline/2
    margin: 0 auto
    margin-bottom: $baseline

    background: #fff
    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 1.5

</style>
