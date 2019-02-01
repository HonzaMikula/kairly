<template>
  <div class="kairly-promo">
    <div>
      <h2><nuxt-link to="/">Kairly</nuxt-link></h2>
      <p>Čtěte jen to, co vás zajímá.</p>

      <div class="kairly-promo--learn-more">
        <nuxt-link to="/">{{ $t('Learn more about the platform') }}</nuxt-link>
      </div>

      <div class="kairly-promo--social-media">
        <a
          href="https://www.facebook.com/kairlynews/"
          class="facebook"
          :title="$t('Follow us on Facebook')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>

        <a
          href="https://twitter.com/kairlynews"
          class="twitter"
          :title="$t('Follow us on Twitter')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>

        <a
          href="https://www.linkedin.com/company/kairly/"
          class="linkedin"
          :title="$t('Follow us on LinkedIn')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'KairlyPromo'
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Kairly Promo -//

.kairly-promo
  position: relative

  display: flex
  align-items: center
  justify-content: center
  height: 400px
  padding: $baseline

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

//- Learn more links
.kairly-promo--learn-more
  display: table
  margin: 0 auto

  a
    +button(primary, large)


//- Social media links
.kairly-promo--social-media
  display: flex
  justify-content: center
  margin-top: $baseline

  a
    border-radius: 100%
    display: inline-block
    height: $baseline * 1.5
    margin: 0 $baseline/2
    width: $baseline * 1.5

    background: #fff
    color: #555

    font-size: $fs-3
    line-height: $baseline * 1.5
    text-align: center

    transition: 0.15s all

    &:focus,
    &:hover
      color: #000

    &::before
      +fa-icon()
      @extend .fab
      line-height: $baseline * 1.5
      vertical-align: top

    &.facebook::before
      content: fa-content($fa-var-facebook)

    &.twitter::before
      content: fa-content($fa-var-twitter)

    &.linkedin::before
      content: fa-content($fa-var-linkedin)
</style>
