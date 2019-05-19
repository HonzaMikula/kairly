<template>
  <div class="kairly-promo">
    <div>
      <section class="kairly-promo--info">
        <h2><nuxt-link to="/">Kairly</nuxt-link></h2>
        <p>
          <nuxt-link to="/rss-reader">
            {{ $t('Stop be distracted.') }}
          </nuxt-link>
        </p>

        <p>
          <nuxt-link to="/rss-reader">
            {{ $t('Import your RSS feeds.') }}
          </nuxt-link>
        </p>
        
        <p>
          <nuxt-link to="/rss-reader">
            {{ $t('Set when you want to read what content.') }}
            <!-- Nastavte si, kdy chcete číst jaký obsah. -->
          </nuxt-link>
        </p>
        
        <p>
          <nuxt-link to="/rss-reader">
            {{ $t('Grow healthy reading habits.') }}
            <!-- Vytvořte si dobré návyky při čtení. -->
          </nuxt-link>
        </p>

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
      </section>

      <SignUpForm></SignUpForm>
    </div>
  </div>
</template>

<script>
import SignUpForm from '@/components/microsite/SignUpForm'

export default {
  name: 'KairlyPromo',

  components: {
    SignUpForm
  }
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
  padding: $baseline

  background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover

  > div
    display: grid
    grid-template-columns: 2fr 1fr
    max-width: 900px

    @media (max-width: $mobile)
      grid-template-columns: auto
      grid-row-gap: $baseline 

.kairly-promo--info
  color: #fff

  font-family: $ff-serif
  text-align: left
  
  h2
    display: table
    padding: 0 $baseline/2
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
    margin-bottom: $baseline

    background: #fff
    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 1.5

    a
      color: #000

//- Learn more links
.kairly-promo--learn-more
  display: none

  a
    +button(primary, medium)


//- Social media links
.kairly-promo--social-media
  display: flex
  justify-content: flex-start
  margin-top: $baseline

  a
    border-radius: 100%
    display: inline-block
    height: $baseline * 1.5
    margin-right: $baseline
    width: $baseline * 1.5

    background: #fff
    color: #555

    font-size: $fs-2
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
