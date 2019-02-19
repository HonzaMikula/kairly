<template>
  <section class="microsite-quote">
    <h2>{{ $t('Was said about us.') }}</h2>

    <blockquote>
      <div v-html="$t('@homepage/quote/zouzalik')"></div>
      <!--
      <p>
        Nowadays, when attacks on journalists, including physical ones, are increasing, we need to find a
        sustainable economic model for journalism. Only in this way can we keep independent journalism on
        politicians and large private corporations. And only in this way we can resist the phenomena of fake
        news and ensure that the complete freedom of speech is preserved.
      </p>

      <p>
        Kairly comes up with an interesting concept of paid content on the internet, which is significantly
        different from the current not very successful attempts.
      </p>
        -->

      <footer>
        <img src="https://pbs.twimg.com/profile_images/762976177535475712/JfzxZ0RA_400x400.jpg" alt="Marek Zouzalík" />
        <strong>Marek Zouzalík</strong> <a href="https://www.sncr-praha.cz/" target="_blank">{{ $t('chairman of the Prague Syndicate of Journalists') }}</a>
      </footer>
    </blockquote>
  </section>
</template>

<script>

export default {
  name: 'QuoteZouzalik'
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

.microsite-quote
  padding: $baseline*2
  margin-bottom: $baseline * 2

  background: #f5f5f5

  @media (max-width: 950px)
    margin-bottom: 0

  @media (max-width: $mobile)
    padding: $baseline

  h2
    +heading
    margin-bottom: $baseline

  blockquote
    p
      margin-bottom: $baseline

      font-size: $fs-2

      @media (max-width: $mobile)
        font-size: $fs-1

      &:first-of-type::before
        +fa-icon()
        @extend .fas
        position: absolute
        transform: translateX(-20px)
        font-size: $fs--2

        color: #555

        content: fa-content($fa-var-quote-left)

      &:last-of-type::after
        +fa-icon()
        @extend .fas

        position: absolute
        font-size: $fs--2
        transform: translateX(5px)

        color: #555

        content: fa-content($fa-var-quote-right)


    footer
      display: flex

      font-size: $fs-1
      line-height: $baseline * 1.5

      a
        color: #000

        text-decoration: underline

        &:hover,
        &:focus
          text-decoration: none

      @media (max-width: $mobile)
        flex-direction: column
        align-items: center

        line-height: $baseline
        text-align: center

      strong::after
        margin-right: 4px

        font-weight: 600

        content: ', '

        @media (max-width: $mobile)
          content: none

      img
        margin-right: $baseline / 2
        border-radius: 100%
        height: $baseline * 1.5
        width: $baseline * 1.5

        @media (max-width: $mobile)
          height: $baseline * 2
          margin-right: 0
          width: $baseline * 2



</style>
