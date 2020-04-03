<template>
  <footer class="microsite-footer-links">
    <div class="microsite-footer-links--social-media">
      <a
        v-b-tooltip
        href="https://www.facebook.com/kairlynews/"
        class="facebook"
        :title="$t('Follow us on Facebook')"
      />

      <a
        v-b-tooltip
        href="https://twitter.com/kairlynews"
        class="twitter"
        :title="$t('Follow us on Twitter')"
      />

      <a
        v-b-tooltip
        href="https://www.linkedin.com/company/kairly/"
        class="linkedin"
        :title="$t('Follow us on LinkedIn')"
      />
    </div>

    <div>
      <a href="mailto:info@kairly.com">info@kairly.com</a> |
      <nuxt-link to="/privacy-policy">{{ $t('Privacy policy') }}</nuxt-link>
    </div>

    <div class="microsite-footer-links--switch-language">
      {{ $t('Switch language') }}
      <a
        href="?lang=cs"
        :class="{'is-active': currentLocale == 'cs'}"
        @click.prevent="setLang('cs')"
      >
        Česky</a>
      <a
        href="?lang=en"
        :class="{'is-active': currentLocale == 'en'}"
        @click.prevent="setLang('en')"
      >
        English</a>

    </div>
  </footer>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'FooterLinks',

  computed: {
    ...mapState({
      currentLocale: state => state.locale || 'en'
    }),
  },

  methods: {
    setLang (locale) {
      this.setLocale(locale)
      this.$auth.$storage.setUniversal('locale', locale)
      this.$ga.event({
        eventCategory: 'Switch language',
        eventAction: locale
      })
    }
  }
}
</script>

<style lang="sass">
//- Footer Links
.microsite-footer-links
  display: flex
  justify-content: space-between
  align-items: center
  max-width: 900px
  margin: 0 auto
  padding: $baseline / 2

  text-align: center

  @media (max-width: $mobile)
    flex-direction: column

  a
    color: $c-base
    text-decoration: underline

    &:hover,
    &:focus
      text-decoration: none

//- Social media links
.microsite-footer-links--social-media
  display: flex
  justify-content: center

  a
    display: inline-block
    height: $baseline * 1.5
    margin-right: $baseline/2
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

//- Switch Language
.microsite-footer-links--switch-language
  a.is-active
    color: #000
    font-weight: 600
    text-decoration: none

  a:first-of-type
    margin-right: $baseline / 4
</style>
