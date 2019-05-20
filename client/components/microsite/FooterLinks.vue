<template>
  <footer class="microsite-footer-links">
    <div>
      <h3>{{ $t('Kairly is platform for') }}</h3>
      <ul>
        <li><nuxt-link to="/readers">{{ $t('Readers') }}</nuxt-link></li>
        <li><nuxt-link to="/journalists">{{ $t('Journalists and bloggers') }}</nuxt-link></li>
        <li><nuxt-link to="/publishers">{{ $t('Publishers') }}</nuxt-link></li>
        <li><nuxt-link to="/think-tanks">{{ $t('Think-tanks and NGOs') }}</nuxt-link></li>
      </ul>
    </div>

    <div>
      <h3>{{ $t('Last posts on blog') }}</h3>
      <ul>
        <li>
          <a href="https://kairly.com/janmikula/proc-soucasne-modely-placeneho-obsahu-selhavaji--2bb1c61a3">
            Proč selhávají současné modely placeného obsahu na internetu?
          </a>
        </li>
        <li>
          <a href="https://kairly.com/janmikula/zurnalistika-v-zajeti-reklamy-existuje-cesta-ven--c2ed80354">
            Žurnalistika v zajetí reklamy. Existuje cesta ven?
          </a>
        </li>
      </ul>
    </div>

    <div>
      <h3>{{ $t('Contact us') }}</h3>

      <ul>
        <li itemprop="email"><a href="mailto:info@kairly.com">info@kairly.com</a></li>
        <li itemprop="telephone" class="phone"><a href="tel:+420739222781">+420 739 222 781</a></li>
      </ul>
    </div>

    <div>
      <h3>{{ $t('Language') }}</h3>
      <ul>
        <li>
          <a
            href="?lang=cs"
            @click.prevent="setLang('cs')"
            :class="{'is-active': currentLocale == 'cs'}">
            Česky
          </a>
        </li>
        <li>
          <a
            href="?lang=en"
            @click.prevent="setLang('en')"
            :class="{'is-active': currentLocale == 'en'}">
            English
          </a>
        </li>
      </ul>
    </div>

  </footer>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'FooterLinks',

  methods: {
    setLang(locale) {
      this.setLocale(locale)
      this.$auth.$storage.setUniversal('locale', locale)
    }
  },

  computed: {
    ...mapState({
      currentLocale: state => state.locale || 'en'
    }),
  },
}
</script>

<style lang="sass">
//- Footer Links
.microsite-footer-links
  display: flex
  justify-content: space-between
  padding: $baseline 0
  max-width: 900px
  margin: auto

  @media (max-width: $mobile)
    flex-direction: column
    padding: $baseline

  div
    margin-right: $baseline

    @media (max-width: $mobile)
      margin-bottom: $baseline

    &:last-of-type
      margin-right: 0

    &:first-of-type li
      white-space: nowrap

  h3
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600
    white-space: nowrap

  li
    margin-bottom: $baseline / 4

    line-height: 1.42

    &.coming-soon
      color: #999

  .phone
    white-space: nowrap

  a
    color: darken($c-base, 20%)

    &:hover,
    &:focus
      color: #000

    &.nuxt-link-exact-active,
    &.is-active
      color: #000

      font-weight: 600
      text-decoration: none
</style>
